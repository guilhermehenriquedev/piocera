function showRelatedObjectPopup(triggeringLink, window_name) {
    var win = window.open(triggeringLink, window_name, 'height=500,width=800,resizable=yes,scrollbars=yes');
    win.focus();
    return false;
}

CKEDITOR.plugins.add('grafico',
    {
        icons: "grafico",
        init: function (a) {
            // Plugin logic goes here...

            a.addCommand('insertGrafico', {
                exec: function (a) {
                    showRelatedObjectPopup('/admin/poll/poll/?_to_field=id&_popup=1', a.name);
                }
            });

            a.ui.addButton('Grafico', {
                label: 'Inserir Grafico no Texto',
                command: 'insertGrafico',
                toolbar: 'insert'
            });

        }
    })
;

