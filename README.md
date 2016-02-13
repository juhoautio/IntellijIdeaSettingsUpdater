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

Usage? just run
```sh
python updater.py --help
```

## Usage examples

You have two IDEA projects in a directory called `IdeaProjects`. They have the following `workspace.xml` settings files:
```sh
~/IdeaProjects/importAutomatically/.idea/workspace.xml
~/IdeaProjects/no_maven_settings/.idea/workspace.xml
```

To update the maven import settings for these projects, run the following command:
```sh
python updater.py -d ~/IdeaProjects
```

Or you can manually tell which files to update:
```sh
python updater.py ~/IdeaProjects/importAutomatically/.idea/workspace.xml ~/IdeaProjects/no_maven_settings/.idea/workspace.\
xml
```

## Safety

A backup is always created before modifying the original file (`workspace.xml-bak`). In case you need to revert the changes..

## Future work

- Making the script generic so that other settings changes can be requested with a simple syntax
  - for example:
```sh
python updater.py --set-value component[@name='MavenImportPreferences']/option[@name='importingSettings']/MavenImportingSe\
ttings/option/[@name='downloadDocsAutomatically']/value=true
```
  - or for example a specialized feature for setting options, something like this:
```sh
python updater.py --set-option MavenImportPreferences/importingSettings/MavenImportingSettings/option/downloadDocsAutomati\
cally=true
```
- Improving the unit test & script structure
- Change tests like `if not maven` to future-proof, for example this:
```sh
python updater.py:93: FutureWarning: The behavior of this method will change in future versions.  Use specific 'len(elem)'\
or 'elem is not None' test instead.
  if not maven:
```
