CKEDITOR.dialog.add('embedCodeNativeDialog', function (editor) {
    return {
        title: 'Incorporar Embed',
        minWidth: 370,
        minHeight: 154,
        contents: [
            {
                id: 'tab-basic',
                label: 'Basic Settings',
                elements: [
                    {
                        type: 'textarea',
                        id: 'embed',
                        label: 'Código do Embed',
                        validate: CKEDITOR.dialog.validate.notEmpty("O campo Código do Embed não pode ser vazio.")
                    }
                ]
            }
        ],
        onOk: function () {
            let dialog = this;
            let embed = dialog.getValueOf('tab-basic', 'embed');
            console.log(embed);
            editor.insertHtml('<p>' + embed + '</p>');
        }
    };
});