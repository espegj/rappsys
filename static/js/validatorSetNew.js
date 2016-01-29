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
            },
            pas: {
                validators: {
                    notEmpty: {
                        message: 'Må fylles inn'
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
                    },
                    identical: {
                        field: 'password_confirm',
                        message: 'Passordene må være like'
                }
                }
            },
            password_confirm: {
                validators: {
                    notEmpty: {
                        message: 'Passord er påkrevd'
                    },
                    identical: {
                        field: 'password',
                        message: 'Passordene må være like'
                }
            }
        }
        }
    });
});