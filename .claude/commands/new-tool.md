# New Tool Generator

Generiere ein komplettes MCP-Tool-Package aus einer Story-YAML-Datei.

## Argument

$ARGUMENTS = Pfad zur Story-YAML (z.B. `stories/docker.yaml`)

## Anweisungen

Du bist der MCP Tool Generator. Deine Aufgabe: Aus einer Story-YAML ein vollständiges, installierbares MCP-Tool-Package erzeugen.

### Schritt 1 — Story lesen und validieren

Lies die Datei `$ARGUMENTS` und prüfe:
- `name`: vorhanden, lowercase, nur `[a-z0-9_]`
- `description`: vorhanden
- `tools`: mindestens 1 Tool, jedes mit `name` + `description`
- `params`: falls vorhanden, jeder mit `name` + `type`
- Keine doppelten Tool-Namen

Falls Fehler: auflisten und abbrechen.

### Schritt 2 — Plan anzeigen

Zeige dem User:
- Package-Name (`mcp-{name}-tools`)
- Modul-Name (`mcp_{name}_tools`)
- Anzahl Tools
- Ob ein Client generiert wird (wenn `client:` in der Story)
- Liste der Dateien die erstellt werden

**Warte auf Bestätigung** bevor du weitermachst.

### Schritt 3 — Generieren

Führe den Generator aus:

```bash
python3 scripts/new-tool.py "$ARGUMENTS"
```

Falls das Zielverzeichnis schon existiert, frage den User ob `--force` verwendet werden soll.

### Schritt 4 — Verifizieren

1. Prüfe ob alle Dateien erstellt wurden
2. Installiere das Package im Editable-Mode:
   ```bash
   pip install -e {name}/
   ```
3. Führe die generierten Tests aus:
   ```bash
   pytest tests/test_{name}/ -v
   ```

### Schritt 5 — Zusammenfassung

Zeige:
- Erstellte Dateien
- Test-Ergebnis
- Nächste Schritte (Tools implementieren, Client implementieren falls vorhanden)

## Regeln

- NIEMALS den Generator umgehen und Dateien manuell schreiben
- IMMER erst Plan zeigen, dann bestätigen lassen
- Bei Fehlern im Generator: Generator fixen, nicht drumherum arbeiten
- Die generierten `tools.py` Funktionen enthalten `raise NotImplementedError` — das ist Absicht
