Intellij Idea Settings Updater
===========================

A python script that modifies the maven import settings in IntelliJ IDEA's `workspace.xml`

It ensures that the following Maven Import preferences are set:

```xml
  <component name="MavenImportPreferences">
    <option name="importingSettings">
      <MavenImportingSettings>
        <option name="downloadDocsAutomatically" value="true" />
        <option name="downloadSourcesAutomatically" value="true" />
        <option name="importAutomatically" value="true" />
      </MavenImportingSettings>
    </option>
  </component>
```

If the element exists previously, it is updated. However, if it previously contains any other options than
`importAutomatically`, the script doesn't modify the file.

Download `updater.py` and make it executable:
```sh
chmod u+x updater.py
```

Usage? just run
```sh
./updater.py --help
```

## Usage examples

You have two IDEA projects in a directory called `IdeaProjects`. They have the following `workspace.xml` settings files:
```
~/IdeaProjects/importAutomatically/.idea/workspace.xml
~/IdeaProjects/no_maven_settings/.idea/workspace.xml
```

To update the maven import settings for these projects, run the following command:
```sh
./updater.py -d ~/IdeaProjects
```

Or you can manually tell which files to update:
```sh
./updater.py ~/IdeaProjects/importAutomatically/.idea/workspace.xml ~/IdeaProjects/no_maven_settings/.idea/workspace.xml
```

## Future work

- Making the script generic so that other settings changes can be requested with a simple syntax
  - for example:
```sh
./updater.py --set-value component[@name='MavenImportPreferences']/option[@name='importingSettings']/MavenImportingSettings/option/[@name='downloadDocsAutomatically']/value=true
```
  - or for example a specialized feature for setting options, something like this:
```sh
./updater.py --set-option MavenImportPreferences/importingSettings/MavenImportingSettings/option/downloadDocsAutomatically=true
```
- Improving the unit test & script structure