"""Tests for mcp-homematic-tools.

Two test modes:
- **Mock tests** (default): Run without any hardware. Test all write operations
  and tool logic using a mock CCU client.
- **Live tests** (opt-in): Read-only tests against a real CCU. Require:
  - Environment variable CCU_URL set (e.g. http://192.168.178.53)
  - Environment variable CCU_USER set (default: Admin)
  - Environment variable CCU_PASSWORD set
  - Network access to the CCU

Run mock tests only (default, no hardware needed):
    pytest tests/test_homematic/

Run live tests too:
    CCU_URL=http://192.168.178.53 CCU_USER=Admin CCU_PASSWORD=secret pytest tests/test_homematic/ --run-live

The --run-live flag is registered via conftest.py.
"""

import json
import os
import pytest
from unittest.mock import MagicMock, patch, call

from mcp_homematic_tools.homematic.client import CCUClient, CCUError
from mcp_homematic_tools.homematic import register
from mcp_homematic_tools.homematic import tools


# ---------------------------------------------------------------------------
# Live test marker — skip unless --run-live + env vars set
# ---------------------------------------------------------------------------

CCU_URL = os.environ.get("CCU_URL", "")
CCU_USER = os.environ.get("CCU_USER", "Admin")
CCU_PASS = os.environ.get("CCU_PASSWORD", "")

# Known IDs — only relevant when running against the reference CCU
DEVICE_ID = "2357"                         # Arbeitszimmer-Fensterkontakt
CHANNEL_ID = "2386"                        # Arbeitszimmer-Fensterkontakt:1
THERMOSTAT_ADDR = "0039A2699EC589:1"       # Arbeitszimmer-Thermostat:1
CONTACT_ADDR = "003664099D8FA5:1"          # Arbeitszimmer-Fensterkontakt:1
ROOM_ID = "1229"                           # Büro
FUNCTION_ID = "1215"                       # Heizung
SYSVAR_ID = "950"                          # Anwesenheit
INTERFACE = "HmIP-RF"

live = pytest.mark.skipif(
    not CCU_URL or not CCU_PASS,
    reason="Live tests require CCU_URL and CCU_PASSWORD env vars (and --run-live flag)",
)


@pytest.fixture(scope="module")
def client():
    """Live CCU client for read-only tests. Skipped if env not configured."""
    if not CCU_URL or not CCU_PASS:
        pytest.skip("CCU_URL / CCU_PASSWORD not set")
    c = CCUClient(CCU_URL, CCU_USER, CCU_PASS)
    yield c
    c.close()


@pytest.fixture
def mock_client():
    """Mock client for write tests."""
    c = MagicMock(spec=CCUClient)
    c.call.return_value = {}
    c.call_interface.return_value = {}
    return c


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------

class TestRegistration:
    def test_register_callable(self):
        assert callable(register)

    def test_register_tools(self):
        from mcp.server.fastmcp import FastMCP
        mcp = FastMCP("test")
        register(mcp, {"url": "http://dummy", "username": "u", "password": "p"})
        registered = [t for t in mcp._tool_manager._tools.keys() if t.startswith("ccu_")]
        assert len(registered) == 60

    def test_register_requires_url(self):
        from mcp.server.fastmcp import FastMCP
        mcp = FastMCP("test")
        with pytest.raises(ValueError, match="url"):
            register(mcp, {})


# ---------------------------------------------------------------------------
# Client
# ---------------------------------------------------------------------------

@live
class TestClient:
    def test_login(self, client):
        """Live: login returns a session ID."""
        client._session_id = None
        sid = client._login()
        assert sid and len(sid) > 5

    def test_call_auto_session(self, client):
        """Live: call() manages sessions transparently."""
        result = client.call("CCU.getVersion")
        assert "3." in str(result)

    def test_call_interface_shorthand(self, client):
        result = client.call_interface("listInterfaces", "")
        assert isinstance(result, list)

    def test_ccu_error(self):
        e = CCUError(502, "test error")
        assert e.code == 502
        assert "test error" in str(e)


# ---------------------------------------------------------------------------
# Live read-only tests — Device
# ---------------------------------------------------------------------------

@live
class TestDeviceLive:
    def test_device_list(self, client):
        result = json.loads(tools.device_list(client))
        assert isinstance(result, list)
        assert len(result) >= 15

    def test_device_list_detail(self, client):
        result = json.loads(tools.device_list(client, detail=True))
        assert isinstance(result, list)
        assert "channels" in result[0]

    def test_device_get(self, client):
        result = json.loads(tools.device_get(client, DEVICE_ID))
        assert result["id"] == DEVICE_ID
        assert "name" in result
        assert "address" in result

    def test_device_status(self, client):
        result = json.loads(tools.device_status(client, DEVICE_ID))
        assert "RSSI_DEVICE" in result or "LOW_BAT" in result


# ---------------------------------------------------------------------------
# Live read-only tests — Channel
# ---------------------------------------------------------------------------

@live
class TestChannelLive:
    def test_channel_value(self, client):
        result = tools.channel_value(client, CHANNEL_ID)
        assert result is not None

    def test_channel_info(self, client):
        result = json.loads(tools.channel_info(client, CHANNEL_ID))
        assert result["id"] == CHANNEL_ID
        assert "type" in result

    def test_channel_programs(self, client):
        result = tools.channel_programs(client, CHANNEL_ID)
        assert "not used" in result or "programIds" in result


# ---------------------------------------------------------------------------
# Live read-only tests — Interface Values
# ---------------------------------------------------------------------------

@live
class TestInterfaceValuesLive:
    def test_get_value_state(self, client):
        result = json.loads(tools.get_value(client, INTERFACE, CONTACT_ADDR, "STATE"))
        assert "value" in result

    def test_get_value_temperature(self, client):
        result = json.loads(tools.get_value(client, INTERFACE, THERMOSTAT_ADDR, "ACTUAL_TEMPERATURE"))
        temp = float(result["value"])
        assert -10 < temp < 50

    def test_get_paramset_values(self, client):
        result = json.loads(tools.get_paramset(client, INTERFACE, THERMOSTAT_ADDR, "VALUES"))
        assert "ACTUAL_TEMPERATURE" in result

    def test_get_paramset_master(self, client):
        result = json.loads(tools.get_paramset(client, INTERFACE, THERMOSTAT_ADDR, "MASTER"))
        assert isinstance(result, dict)
        assert len(result) > 5

    def test_get_paramset_desc(self, client):
        result = json.loads(tools.get_paramset_desc(client, INTERFACE, THERMOSTAT_ADDR, "VALUES"))
        assert isinstance(result, dict)

    def test_get_master_value(self, client):
        result = json.loads(tools.get_master_value(client, INTERFACE, THERMOSTAT_ADDR, "TEMPERATURE_OFFSET"))
        assert "value" in result


# ---------------------------------------------------------------------------
# Live read-only tests — Interface Diagnostics
# ---------------------------------------------------------------------------

@live
class TestInterfaceDiagnosticsLive:
    def test_list_interfaces(self, client):
        result = json.loads(tools.list_interfaces(client))
        names = [i["name"] for i in result]
        assert "HmIP-RF" in names

    def test_list_devices_raw(self, client):
        result = json.loads(tools.list_devices_raw(client, INTERFACE))
        assert isinstance(result, list)
        assert len(result) > 10

    def test_device_description(self, client):
        result = json.loads(tools.device_description(client, INTERFACE, "0039A2699EC589"))
        assert isinstance(result, dict)

    def test_rssi_all(self, client):
        result = json.loads(tools.rssi(client))
        assert isinstance(result, dict)
        assert len(result) > 0

    def test_rssi_interface(self, client):
        result = json.loads(tools.rssi(client, INTERFACE))
        assert isinstance(result, (dict, list))

    def test_duty_cycle(self, client):
        result = json.loads(tools.duty_cycle(client))
        assert isinstance(result, list)

    def test_service_messages_count(self, client):
        result = json.loads(tools.service_messages(client, "count"))
        assert isinstance(result, dict)

    def test_service_messages_count_interface(self, client):
        result = json.loads(tools.service_messages(client, "count", INTERFACE))
        assert "serviceMessageCount" in result

    def test_service_messages_list_suppressed(self, client):
        result = json.loads(tools.service_messages(client, "list_suppressed"))
        assert isinstance(result, list)


# ---------------------------------------------------------------------------
# Live read-only tests — Pairing (status only)
# ---------------------------------------------------------------------------

@live
class TestPairingLive:
    def test_add_device_status(self, client):
        result = json.loads(tools.add_device(client, "status", INTERFACE))
        assert "installModeSecondsLeft" in result

    def test_links(self, client):
        result = json.loads(tools.links(client, INTERFACE, CONTACT_ADDR, 0))
        assert isinstance(result, list)

    def test_set_bidcos_interface_list(self, client):
        result = json.loads(tools.set_bidcos_interface(client, "list"))
        assert isinstance(result, list)


# ---------------------------------------------------------------------------
# Live read-only tests — Room / Function
# ---------------------------------------------------------------------------

@live
class TestRoomLive:
    def test_room_list(self, client):
        result = json.loads(tools.room_list(client))
        names = [r["name"] for r in result]
        assert "Wohnzimmer" in names

    def test_room_get(self, client):
        result = json.loads(tools.room_get(client, ROOM_ID))
        assert result["id"] == ROOM_ID
        assert "channelIds" in result

    def test_function_list(self, client):
        result = json.loads(tools.function_list(client))
        names = [f["name"] for f in result]
        assert "Heizung" in names

    def test_function_get(self, client):
        result = json.loads(tools.function_get(client, FUNCTION_ID))
        assert result["id"] == FUNCTION_ID


# ---------------------------------------------------------------------------
# Live read-only tests — SysVar
# ---------------------------------------------------------------------------

@live
class TestSysVarLive:
    def test_sysvar_list(self, client):
        result = json.loads(tools.sysvar_list(client))
        names = [v["name"] for v in result]
        assert "Anwesenheit" in names

    def test_sysvar_get_by_id(self, client):
        result = json.loads(tools.sysvar_get(client, id=SYSVAR_ID))
        assert result["name"] == "Anwesenheit"

    def test_sysvar_get_by_name(self, client):
        result = json.loads(tools.sysvar_get(client, name="DutyCycle"))
        assert "value" in result


# ---------------------------------------------------------------------------
# Live read-only tests — Program, System, ReGa, Firewall
# ---------------------------------------------------------------------------

@live
class TestSystemLive:
    def test_program_list(self, client):
        result = tools.program_list(client)
        assert "No programs" in result or isinstance(json.loads(result), list)

    def test_system_info(self, client):
        result = json.loads(tools.system_info(client))
        assert "3." in result["version"]

    def test_heating_groups(self, client):
        result = tools.heating_groups(client)
        assert result is not None

    def test_rega_status(self, client):
        result = json.loads(tools.rega_status(client))
        assert "regaPresent" in result

    def test_rega_datapoints(self, client):
        result = json.loads(tools.rega_datapoints(client))
        assert isinstance(result, list)

    def test_firewall_get(self, client):
        result = json.loads(tools.firewall(client, "get"))
        assert isinstance(result, dict)


# ---------------------------------------------------------------------------
# Live read-only tests — Convenience
# ---------------------------------------------------------------------------

@live
class TestConvenienceLive:
    def test_climate_all(self, client):
        result = json.loads(tools.climate(client))
        assert isinstance(result, list)
        assert any("temperature" in d for room in result for d in room["devices"])

    def test_climate_filtered(self, client):
        result = json.loads(tools.climate(client, "Büro"))
        assert len(result) == 1
        assert result[0]["room"] == "Büro"

    def test_climate_no_match(self, client):
        result = tools.climate(client, "Keller")
        assert "No climate data" in result

    def test_windows_all(self, client):
        result = json.loads(tools.windows(client))
        assert isinstance(result, list)
        for room in result:
            for c in room["contacts"]:
                assert c["state"] in ("open", "closed")

    def test_windows_filtered(self, client):
        result = json.loads(tools.windows(client, "Küche"))
        assert len(result) == 1

    def test_windows_state_logic(self, client):
        """Verify STATE=0 means closed, STATE=1 means open."""
        result = json.loads(tools.windows(client))
        for room in result:
            for c in room["contacts"]:
                if str(c["rawState"]) == "0":
                    assert c["state"] == "closed"
                elif str(c["rawState"]) == "1":
                    assert c["state"] == "open"


# ---------------------------------------------------------------------------
# Live read-only tests — Events
# ---------------------------------------------------------------------------

@live
class TestEventsLive:
    def test_event_lifecycle(self, client):
        sub = json.loads(tools.event_subscribe(client, "subscribe"))
        assert sub.get("subscribed") is True

        poll = tools.event_poll(client)
        assert poll is not None

        unsub = json.loads(tools.event_subscribe(client, "unsubscribe"))
        assert unsub.get("subscribed") is False


# ===========================================================================
# Mock tests for write operations
# ===========================================================================

class TestDeviceWriteMock:
    def test_device_set_name(self, mock_client):
        result = tools.device_set_name(mock_client, "123", "NewName")
        mock_client.call.assert_called_with("Device.setName", {"id": "123", "name": "NewName"})
        assert "NewName" in result

    def test_device_set_visibility(self, mock_client):
        result = tools.device_set_visibility(mock_client, "123", visibility="true")
        mock_client.call.assert_called_with(
            "Device.setVisibility", {"id": "123", "isVisible": True}
        )
        assert "visibility=true" in result

    def test_device_set_visibility_multiple(self, mock_client):
        tools.device_set_visibility(
            mock_client, "123",
            visibility="true", operate_group_only="false", enabled_service_msg="true",
        )
        assert mock_client.call.call_count == 3

    def test_device_set_visibility_empty(self, mock_client):
        result = tools.device_set_visibility(mock_client, "123")
        assert "No settings" in result
        mock_client.call.assert_not_called()

    def test_device_comtest_start(self, mock_client):
        mock_client.call.return_value = "test-42"
        result = json.loads(tools.device_comtest(mock_client, "123", "start"))
        assert result["testId"] == "test-42"


class TestChannelWriteMock:
    def test_channel_set_name(self, mock_client):
        result = tools.channel_set_name(mock_client, "456", "NewChannel")
        mock_client.call.assert_called_with("Channel.setName", {"id": "456", "name": "NewChannel"})
        assert "NewChannel" in result

    def test_channel_config_logging(self, mock_client):
        tools.channel_config(mock_client, "456", logging="true")
        mock_client.call.assert_called_with(
            "Channel.setLogging", {"id": "456", "isLogged": True}
        )

    def test_channel_config_empty(self, mock_client):
        result = tools.channel_config(mock_client, "456")
        assert "No settings" in result


class TestInterfaceWriteMock:
    def test_set_value_double(self, mock_client):
        tools.set_value(mock_client, "HmIP-RF", "ADDR:1", "SET_POINT_TEMPERATURE", "21.5", "double")
        mock_client.call_interface.assert_called_with(
            "setValue", "HmIP-RF", "ADDR:1",
            valueKey="SET_POINT_TEMPERATURE", type="double", value=21.5,
        )

    def test_set_value_bool(self, mock_client):
        tools.set_value(mock_client, "HmIP-RF", "ADDR:1", "BOOST_MODE", "true", "bool")
        mock_client.call_interface.assert_called_with(
            "setValue", "HmIP-RF", "ADDR:1",
            valueKey="BOOST_MODE", type="bool", value=True,
        )

    def test_set_value_int(self, mock_client):
        tools.set_value(mock_client, "HmIP-RF", "ADDR:1", "DURATION", "3600", "int")
        mock_client.call_interface.assert_called_with(
            "setValue", "HmIP-RF", "ADDR:1",
            valueKey="DURATION", type="int", value=3600,
        )

    def test_put_paramset(self, mock_client):
        tools.put_paramset(mock_client, "HmIP-RF", "ADDR:1", "VALUES", '{"KEY": 42}')
        mock_client.call_interface.assert_called_with(
            "putParamset", "HmIP-RF", "ADDR:1",
            paramsetKey="VALUES", set={"KEY": 42},
        )

    def test_delete_device(self, mock_client):
        result = tools.delete_device(mock_client, "HmIP-RF", "ADDR", 0)
        mock_client.call_interface.assert_called_with("deleteDevice", "HmIP-RF", "ADDR", flags=0)
        assert "deleted" in result

    def test_change_device(self, mock_client):
        result = tools.change_device(mock_client, "HmIP-RF", "OLD", "NEW")
        assert "replaced" in result

    def test_add_link(self, mock_client):
        result = tools.add_link(mock_client, "HmIP-RF", "S:1", "R:1", "MyLink", "desc")
        assert "created" in result
        assert mock_client.call_interface.call_count == 2  # addLink + setLinkInfo

    def test_remove_link(self, mock_client):
        result = tools.remove_link(mock_client, "HmIP-RF", "S:1", "R:1")
        assert "removed" in result

    def test_config_cache_clear(self, mock_client):
        result = tools.config_cache(mock_client, "clear", "HmIP-RF", "ADDR")
        assert "cleared" in result

    def test_config_cache_restore(self, mock_client):
        result = tools.config_cache(mock_client, "restore", "HmIP-RF", "ADDR")
        assert "restored" in result

    def test_metadata_set(self, mock_client):
        mock_client.call.return_value = None
        result = tools.metadata(mock_client, "set", "obj1", "key1", "val1")
        assert "set" in result.lower()

    def test_metadata_remove(self, mock_client):
        mock_client.call.return_value = None
        result = tools.metadata(mock_client, "remove", "obj1", "key1")
        assert "removed" in result.lower()

    def test_thermostat_party(self, mock_client):
        result = tools.thermostat_party(mock_client, "HmIP-RF", "ADDR:1", '{"PARTY_TEMP": 25}')
        assert "Party mode" in result

    def test_add_device_enable_mode(self, mock_client):
        result = tools.add_device(mock_client, "enable_mode", "HmIP-RF", mode_duration=120)
        assert "120s" in result

    def test_add_device_add(self, mock_client):
        tools.add_device(mock_client, "add", "HmIP-RF", serial="ABC123")
        mock_client.call_interface.assert_called()

    def test_service_messages_suppress(self, mock_client):
        result = tools.service_messages(mock_client, "suppress", "HmIP-RF", "ADDR:0", "UNREACH")
        assert "suppressed" in result


class TestRoomWriteMock:
    def test_room_channel_add(self, mock_client):
        result = tools.room_channel(mock_client, "add", "1229", "2386")
        mock_client.call.assert_called_with("Room.addChannel", {"id": "1229", "channelId": "2386"})
        assert "added" in result

    def test_room_channel_remove(self, mock_client):
        result = tools.room_channel(mock_client, "remove", "1229", "2386")
        assert "removed" in result

    def test_function_channel_add(self, mock_client):
        result = tools.function_channel(mock_client, "add", "1215", "2386")
        assert "added" in result

    def test_function_channel_remove(self, mock_client):
        result = tools.function_channel(mock_client, "remove", "1215", "2386")
        assert "removed" in result


class TestSysVarWriteMock:
    def test_sysvar_set_bool(self, mock_client):
        mock_client.call.return_value = {"type": "LOGIC", "name": "Anwesenheit"}
        result = tools.sysvar_set(mock_client, "950", "false")
        calls = mock_client.call.call_args_list
        assert calls[1] == call("SysVar.setBool", {"id": "950", "value": False})

    def test_sysvar_set_float(self, mock_client):
        mock_client.call.return_value = {"type": "NUMBER", "name": "DutyCycle"}
        result = tools.sysvar_set(mock_client, "1395", "5.5")
        calls = mock_client.call.call_args_list
        assert calls[1] == call("SysVar.setFloat", {"id": "1395", "value": 5.5})

    def test_sysvar_set_enum(self, mock_client):
        mock_client.call.return_value = {"type": "ENUM", "name": "TestEnum"}
        result = tools.sysvar_set(mock_client, "99", "2")
        calls = mock_client.call.call_args_list
        assert calls[1] == call("SysVar.setEnum", {"id": "99", "value": "2"})

    def test_sysvar_create_bool(self, mock_client):
        result = tools.sysvar_create(mock_client, "TestBool", "bool", "true")
        assert "created" in result

    def test_sysvar_create_float(self, mock_client):
        result = tools.sysvar_create(mock_client, "TestFloat", "float", "0", "0", "100")
        assert "created" in result

    def test_sysvar_create_enum(self, mock_client):
        result = tools.sysvar_create(mock_client, "TestEnum", "enum", "0", enum_values="A;B;C")
        assert "created" in result

    def test_sysvar_delete(self, mock_client):
        result = tools.sysvar_delete(mock_client, "TestVar")
        mock_client.call.assert_called_with("SysVar.deleteSysVarByName", {"name": "TestVar"})
        assert "deleted" in result


class TestProgramWriteMock:
    def test_program_execute(self, mock_client):
        result = tools.program_execute(mock_client, "execute", id="42")
        mock_client.call.assert_called_with("Program.execute", {"id": "42"})
        assert "executed" in result

    def test_program_delete(self, mock_client):
        result = tools.program_execute(mock_client, "delete", name="OldProg")
        mock_client.call.assert_called_with("Program.deleteProgramByName", {"name": "OldProg"})
        assert "deleted" in result

    def test_program_execute_no_id(self, mock_client):
        result = tools.program_execute(mock_client, "execute")
        assert "Error" in result


class TestSystemWriteMock:
    def test_system_config(self, mock_client):
        result = tools.system_config(mock_client, "ssh", "1")
        mock_client.call.assert_called_with("CCU.setSSH", {"mode": 1})
        assert "set" in result.lower()

    def test_system_config_unknown(self, mock_client):
        result = tools.system_config(mock_client, "nonexistent", "x")
        assert "Unknown" in result

    def test_system_restart_rega(self, mock_client):
        result = tools.system_restart(mock_client, "rega")
        mock_client.call.assert_called_with("CCU.restartReGa")
        assert "restarted" in result

    def test_rega_script(self, mock_client):
        mock_client.call.return_value = "script output"
        result = tools.rega_script(mock_client, "Write('hello');")
        mock_client.call.assert_called_with("ReGa.runScript", {"script": "Write('hello');"})

    def test_firewall_set(self, mock_client):
        result = tools.firewall(mock_client, "set", '{"mode": "RESTRICTIVE"}')
        assert "updated" in result

    def test_event_subscribe(self, mock_client):
        mock_client.call.return_value = True
        result = json.loads(tools.event_subscribe(mock_client, "subscribe"))
        assert result["subscribed"] is True

    def test_firmware_refresh(self, mock_client):
        result = tools.firmware(mock_client, "refresh", "HmIP-RF")
        assert "refreshed" in result

    def test_firmware_update(self, mock_client):
        result = tools.firmware(mock_client, "update", "HmIP-RF", "ADDR1,ADDR2")
        assert "started" in result
