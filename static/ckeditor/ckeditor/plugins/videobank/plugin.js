// function showRelatedObjectPopup(triggeringLink, window_name) {
//     var win = window.open(triggeringLink, window_name, 'height=500,width=800,resizable=yes,scrollbars=yes');
//     win.focus();
//     return false;
// }
//
// CKEDITOR.plugins.add('videobank',
//     {
//         icons: "videobank",
//         init: function (a) {
//             // Plugin logic goes here...
//
//             a.addCommand('insertVideoBank', {
//                 exec: function (a) {
//                     showRelatedObjectPopup('/admin/videostream/video/?_to_field=id&_popup=1', a.name);
//                 }
//             });
//
//             a.ui.addButton('VideoBank', {
//                 label: 'Inserir Video do Banco',
//                 command: 'insertVideoBank',
//                 toolbar: 'insert'
//             });
//
//         }
//
//
//     })
// ;
//

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
        .on('load', function () {
            $popup.add($document.find('.related-popup-back')).fadeIn(200, 'swing', function () {
                $loading.hide();
            });
        });

    $popup.append($iframe);
    $loading.show();
    $document.find('.related-popup').add($document.find('.related-popup-back')).fadeOut(200, 'swing');
    $container.fadeIn(200, 'swing', function () {
        $container.append($popup);
    });
    $body.addClass('non-scrollable');
}

CKEDITOR.plugins.add('videobank',
    {
        icons: "videobank",
        init: function (a) {
            // Plugin logic goes here...

            a.addCommand('insertVideoBank', {
                exec: function (a) {
                    popUP(a.name, '/admin/videostream/video/?_to_field=id&_popup=1');
                }

            });

            a.ui.addButton('VideoBank', {
                label: 'Inserir Video do Banco',
                command: 'insertVideoBank',
                toolbar: 'insert'
            });

        }


    })
;

