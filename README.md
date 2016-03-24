supervisor installation

```shell
pip3 install requests psutil
brew install supervisor
mkdir -p /usr/local/etc/supervisor.d
ln -s ~/code/emoncms-linux/supervisor/osx.ini /usr/local/etc/supervisor.d/
```

launchd installation

```shell
sudo ln -s ~/code/emoncms-linux/supervisor/me.swineson.emoncms.reporter.osx.plist /Library/LaunchDaemons/
sudo launchctl load /Library/LaunchDaemons/me.swineson.emoncms.reporter.osx.plist
```
