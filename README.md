testflight
==========

Simple scripts to compile ios/android code and upload directly on
testflight

## basic use:
### Simply compile your project 
`testflight YourXCodeProject` (Compile and generate a ipa)
`testflight YourXcodeProject -t TESTFLIGHT_TEAM_TOKEN -s TESTFLIGHT_TOKEN -c "TESTFLIGHT COMMENT"` (Compile and upload to testflight)

### Using configuration 
You can create a configuration json (default on /etc/testflight/testflight.json) to define a project name and define there all your project 
properties
`testflight ProjectName`


