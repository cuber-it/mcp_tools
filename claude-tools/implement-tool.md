# Implement Tool

Implementiere die Tool-Stubs eines generierten MCP-Packages.

## Argument

$ARGUMENTS = Package-Name (z.B. `docker`) oder Pfad zur Story (z.B. `stories/docker.yaml`)

## Anweisungen

Du bist der MCP Tool Implementierer. Deine Aufgabe: Die `NotImplementedError`-Stubs in einem generierten Package durch funktionierende Implementierungen ersetzen.

### Schritt 1 — Bestandsaufnahme

Ermittle den Package-Namen aus $ARGUMENTS (wenn Story-Pfad: Name aus YAML lesen).

Lies folgende Dateien:
- `stories/{name}.yaml` — Tool-Definitionen, Client-Config, Dependencies
- `{name}/src/mcp_{name}_tools/{name}/tools.py` — aktuelle Stubs
- `{name}/src/mcp_{name}_tools/{name}/client.py` — Client (falls vorhanden)

Zaehle: Wie viele Tools sind noch `NotImplementedError`, wie viele bereits implementiert?

### Schritt 2 — Plan anzeigen

Zeige dem User:
- Package-Name und Anzahl Tools
- Liste der noch nicht implementierten Tools (Name + Description aus Story)
- Welche externen APIs/Libraries verwendet werden
- Vorgeschlagene Reihenfolge (einfache zuerst, abhaengige danach)

**Warte auf Bestaetigung.** Der User kann auch einzelne Tools auswaehlen.

### Schritt 3 — Client implementieren (falls vorhanden)

Wenn `client.py` existiert und noch ein Skeleton ist:
1. Lies die Story fuer `config_keys` und `dependencies`
2. Implementiere die Client-Klasse mit den noetigsten API-Methoden
3. Orientiere dich an den Tools die den Client brauchen

### Schritt 4 — Tools implementieren

Fuer jedes Tool:
1. Lies die Tool-Definition aus der Story (params, description)
2. Implementiere die Funktion in `tools.py`
3. Halte die Signatur exakt wie vom Generator erzeugt
4. Nutze den Client wenn vorhanden, sonst stdlib
5. Gib immer `str` zurueck (MCP-Konvention): JSON-String fuer strukturierte Daten, Klartext fuer einfache Antworten
6. Fehlerbehandlung: fange spezifische Exceptions, gib lesbare Fehlermeldungen zurueck

### Schritt 5 — Tests erweitern

Erweitere `tests/test_{name}/test_{name}.py`:
- Funktionale Tests fuer jedes implementierte Tool
- Mocke externe APIs/Clients wo noetig
- Teste Fehlerfaelle (ungueltige IDs, leere Antworten, Timeouts)

### Schritt 6 — Verifizieren

```bash
pytest tests/test_{name}/ -v
```

Alle Tests muessen gruen sein bevor du weitermachst.

### Schritt 7 — Zusammenfassung

Zeige:
- Implementierte Tools (mit Kurzuebersicht was sie tun)
- Test-Ergebnis
- Offene Punkte (falls nicht alle Tools implementiert wurden)

## Regeln

- IMMER die Signatur aus dem generierten Code beibehalten (Typ-Hints, Defaults)
- IMMER `str` als Rueckgabetyp (MCP-Konvention)
- NIEMALS die `register()` Funktion in `__init__.py` aendern — nur `tools.py` und `client.py`
- Fuer JSON-Rueckgaben: `import json` + `json.dumps(data, indent=2)`
- Externe Dependencies pruefen: Sind sie in `pyproject.toml` gelistet?
- Bei HTTP-Clients: httpx bevorzugen (async-faehig, bereits Dependency)
- ERST Plan zeigen, DANN implementieren
