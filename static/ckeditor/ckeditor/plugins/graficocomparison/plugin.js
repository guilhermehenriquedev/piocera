function showRelatedObjectPopup(triggeringLink, window_name) {
    var win = window.open(triggeringLink, window_name, 'height=500,width=800,resizable=yes,scrollbars=yes');
    win.focus();
    return false;
}

CKEDITOR.plugins.add('graficocomparison',
    {
        icons: "graficocomparison",
        init: function (a) {
            // Plugin logic goes here...

            a.addCommand('insertGraficoComparison', {
                exec: function (a) {
                    showRelatedObjectPopup('/admin/poll/graphcomparison/?_to_field=id&_popup=1', a.name);
                }
            });

            a.ui.addButton('GraficoComparison', {
                label: 'Inserir Grafico Comparativo no Texto',
                command: 'insertGraficoComparison',
                toolbar: 'insert'
            });

        }
    })
;

