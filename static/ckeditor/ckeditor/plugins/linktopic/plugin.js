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

CKEDITOR.plugins.add('linktopic',
    {
        icons: "linktopic",
        init: function (a) {
            // Plugin logic goes here...

            a.addCommand('insertLinkTopic', {
                exec: function (a) {
                    popUP(a.name, '/admin/topic/topic/?_to_field=id&_popup=1');
                }

            });

            a.ui.addButton('LinkTopic', {
                label: 'Inserir Link de Tópico no Texto',
                command: 'insertLinkTopic',
                toolbar: 'insert'
            });

        }


    })
;

