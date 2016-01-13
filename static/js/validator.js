$(document).ready(function() {
    $('#tryitForm').bootstrapValidator({
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
            },
            password: {
                validators: {
                    notEmpty: {
                        message: 'Passord er påkrevd'
                    },
                    stringLength: {
                        min: 6,
                        max: 30,
                        message: 'Passordet må innholde 6 karakterer'
                    }
                }
            }
        }
    });
});