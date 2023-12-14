CKEDITOR.plugins.add( 'embedcodenative', {
    icons: 'embedcodenative',
    init: function( editor ) {
        editor.addCommand( 'embedcodenative', new CKEDITOR.dialogCommand( 'embedCodeNativeDialog' ) );
        editor.ui.addButton('EmbedCodeNative', {
            label: 'Inserir código de Embed',
            command: 'embedcodenative',
            toolbar: 'insert'
        });

        CKEDITOR.dialog.add( 'embedCodeNativeDialog', this.path + 'dialogs/embedcodenative.js' );
    }
});

//https://ckeditor.com/docs/ckeditor4/latest/guide/plugin_sdk_sample_1.html