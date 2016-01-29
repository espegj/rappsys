$(document).ready(function() {
    $('#tryitForm2').bootstrapValidator({
        feedbackIcons: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
            email: {
                validators: {
                    notEmpty: {
                        message: 'Email er påkrevd'
                    },
                    emailAddress: {
                        message: 'Ikke korrekt email'
                    }
                }
            }
        }
    });
});