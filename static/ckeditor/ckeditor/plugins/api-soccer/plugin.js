CKEDITOR.plugins.add('api-soccer',
    {
        icons: "apisoccer",
        init: function (a) {
            // Plugin logic goes here...

            a.addCommand('insertEmbedSoccer', {
                exec: function (a) {
                    popUP(a.name, '/tabelas/ckeditor-jogos/?_popup=1');
                }

            });

            a.ui.addButton('ApiSoccer', {
                label: 'Inserir Embed de Jogos',
                command: 'insertEmbedSoccer',
                toolbar: 'insert'
            });

        }


    })
;

