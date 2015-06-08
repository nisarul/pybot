# PyBot

A plugins-based Python Telegram Bot.

This bot is based on [Telex](https://github.com/datamachine/telex) developed by Vince (@Surye) and Phillip (@Tyrannosaurus)


There are not a lot of useful plugins by default, but you can run ``` !pkg update ``` and then ``` !pkg list all ``` to see what plugins are available to install.

Some plugins require admin permissions. You can set an admin in permissions.conf using the followig format

```
[groups]
  admins = <userid#>,<userid#>,<userid#>
```

You can get your user id number by sending the following query to the bot

```
!tginfo id
```


### Installation
Steps:
1: Clone git repository.
2: Install dependencies
3: Install pybot
4: Setup tg
5: Run pybot

#### Cloning the repository

     git clone --recursive https://github.com/nisarul/pybot.git && pybot

#### Installing dependencies

##### Linux and BSDs

Install libs: readline, openssl and (if you want to use config) libconfig, liblua, python and libjansson.
If you do not want to use them pass options --disable-libconfig, --disable-liblua, --disable-python and --disable-json respectively.

(TESTED ONLY ON Debian 8)

###### On Ubuntu/Debian use: 

     sudo apt-get install libreadline-dev libconfig-dev libssl-dev lua5.2 liblua5.2-dev libevent-dev libjansson-dev python3-dev make 

###### On gentoo:

     sudo emerge -av sys-libs/readline dev-libs/libconfig dev-libs/openssl dev-lang/lua dev-libs/libevent dev-libs/jansson dev-lang/python3

###### On Fedora:

     sudo yum install lua-devel openssl-devel libconfig-devel readline-devel libevent-devel libjansson-devel python3-devel

###### On FreeBSD:

     pkg install libconfig libexecinfo lua52 python3

###### On OpenBSD:

     pkg_add libconfig libexecinfo lua python3

###### On openSUSE:

     sudo zypper in lua-devel libconfig-devel readline-devel libevent-devel libjansson-devel python3-devel libopenssl-devel

#### Installing PyBot
To install the bot, run the following in pybot directory.

     ./launch.sh install

#### Setting up Telegram cli (verifying phone number)
Do the following.

     cd tg
     bin/telegram-cli -k tg-server.pub

It will ask for your phone number and confirmation code.
After successful verificaion of phone number, press Ctrl+C to stop telegram-cli.

#### Running PyBot

To start the bot, run the following in pybot directory.

     ./launch

### Running bot as a service
If you have [upstart](http://upstart.ubuntu.com/), you can run the bot as a service by following the below procedure.

To check if you have upstart, just run 

     sudo start

If output something like this, then you have upstart.

     start: missing job name
     Try `start --help' for more information.
Edit the config file.

     sed -i "s/yourusername/$(whoami)/g" temp/pybot.conf
     sed -i "s_telegrambotpath_$(pwd)_g" temp/pybot.conf
     sudo cp temp/pybot.conf /etc/init/
     sudo start telegram # To start it
     sudo stop telegram # To stop it

