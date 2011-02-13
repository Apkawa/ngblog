# -*- coding: utf-8 -*-

def main():
    import plugin
    plugins = plugin.PluginManager().get_plugins()
    print plugins

    bnw = plugins.get('plugins.bnw')()
    bnw.setup(login_key='234hfudf74')
    print bnw.add_post('Tect bnw api', ['test'])
    print bnw.get_post('G50DMG')
    print bnw.add_reply('Tect bnw api', 'G50DMG')
    print bnw.get_post('G50DMG/7GT')
    print bnw.delete_reply('G50DMG/7GT')
    print bnw.delete_post('SJOF54')



if __name__ == '__main__':
    main()
