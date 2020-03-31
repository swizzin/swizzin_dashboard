![swizzin](http://i.imgur.com/JZlDKP1.png)


# swizzin dashboard v0.1

[website](https://swizzin.ltd) | [docs](https://docs.swizzin.ltd) | [discord](https://discord.gg/bDFqAUF)


### What is this?
This panel offers a quick overview of installed applications, information about their status and information about the server in general. It is written in Python 3 and based on the Flask web server. Its main goals are to be performant, quick and easier to customize than the previous incarnation which was based on the quickbox_dashboard and based on PHP.

### Quick Start:

This package is included in the swizzin repository of applications. To easily install it, you simply need to use box:

```
sudo box install panel
```

If you are adapting this package to work outside of a swizzin environment, the steps necessary for install are outlined in [setup.sh](https://raw.githubusercontent.com/liaralabs/swizzin_dashboard/master/setup.sh)

#### Dependencies

- Python 3.5+
- Flask
- Flask-htpasswd
- Flask-SocketIO
- eventlet

### Support and Help

If you have any questions, please read the [documentation](https://docs.swizzin.ltd/applications/panel) first. If you still have questions or would like to bounce some ideas off other humans, feel free to join us in [discord](https://discord.gg/bDFqAUF).

Do not use GitHub issues for technical support or feature requests. GitHub issues are only to be used to report bugs and other issues with the project.


### Donations

I accept donations on the [project website](https://swizzin.ltd/#donate) and also through [Liberapay](https://liberapay.com/liara/). Please consider a donation if you enjoy the project.

If you don't have spare funds, then you might consider donating the idle cycles on your CPU to my mining pool. Setting it up is easy and will cost you nothing. Simply issue the command:
```
box install xmrig
```
The amount you choose to donate to me is up to you, though the minimum is 1.0. If you need help in setting up your own wallet, check out the [Monero Project](https://getmonero.org).
