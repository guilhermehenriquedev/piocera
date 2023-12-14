function popUP($input, href) {
    var $document = jQuery(window.top.document);
    var $container = $document.find('.related-popup-container');
    var $loading = $container.find('.loading-indicator');
    var $body = $document.find('body');
    var $popup = jQuery('<div>')
        .addClass('related-popup')
        .data('input', $input);
    var $iframe = jQuery('<iframe>')
        .attr('src', href)
        .on('load', function() {
            $popup.add($document.find('.related-popup-back')).fadeIn(200, 'swing', function() {
                $loading.hide();
            });
        });

    $popup.append($iframe);
    $loading.show();
    $document.find('.related-popup').add($document.find('.related-popup-back')).fadeOut(200, 'swing');
    $container.fadeIn(200, 'swing', function() {
        $container.append($popup);
    });
    $body.addClass('non-scrollable');
}

CKEDITOR.plugins.add('imagebank',
    {
        icons: "imagebank",
        init: function (a) {
            // Plugin logic goes here...

            a.addCommand('insertImageBank', {
                exec: function (a) {
                    popUP(a.name, '/admin/image_bank/photo/select/?_to_field=id&_popup=1');
                }

            });

            a.ui.addButton('ImageBank', {
                label: 'Inserir Imagem do Banco',
                command: 'insertImageBank',
                toolbar: 'insert'
            });

        }


    })
;

