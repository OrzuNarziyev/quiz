(function ($) {
    "use strict";

    let input100 = document.querySelectorAll('.input100')

    input100.forEach(e => {
        console.log(e.value)
        if (e.type == 'tel') {
            e.classList.add('has-val')
        }
        if (e.value.length > 1) {
            e.classList.add('has-val')
        }
    })

    /*==================================================================
    [ Focus Contact2 ]*/
    $('.input100').each(function () {
        $(this).on('blur', function () {
            if ($(this).val().trim() != "") {
                $(this).addClass('has-val');
            } else {
                $(this).removeClass('has-val');
            }
        })
    })


    /*==================================================================
    [ Validate ]*/
    // var input = $('.validate-input .input100');
    //
    // $('.validate-form').on('submit', function () {
    //     var check = true;
    //
    //     for (var i = 0; i < input.length; i++) {
    //         if (validate(input[i]) == false) {
    //             showValidate(input[i]);
    //             check = false;
    //         }
    //     }
    //
    //     return check;
    // });


    // $('.validate-form .input100').each(function () {
    //     $(this).focus(function () {
    //         hideValidate(this);
    //     });
    // });

    // function validate(input) {
    //     if ($(input).attr('type') == 'email') {
    //         if ($(input).val().trim().match(/^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{1,5}|[0-9]{1,3})(\]?)$/) == null) {
    //             return false;
    //         }
    //     } else {
    //         if ($(input).val().trim() == '') {
    //             return false;
    //         }
    //     }
    // }

    // function showValidate(input) {
    //     var thisAlert = $(input).parent();
    //
    //     $(thisAlert).addClass('alert-validate');
    // }
    //
    // function hideValidate(input) {
    //     var thisAlert = $(input).parent();
    //
    //     $(thisAlert).removeClass('alert-validate');
    // }


})(jQuery);

// phone mask


function doFormat(x, pattern, mask) {
    var strippedValue = x.replace(/[^0-9]/g, "");
    var chars = strippedValue.split('');
    var count = 0;

    var formatted = '';
    for (var i = 0; i < pattern.length; i++) {
        const c = pattern[i];
        if (chars[count]) {
            if (/\*/.test(c)) {
                formatted += chars[count];
                count++;
            } else {
                formatted += c;
            }
        } else if (mask) {
            if (mask.split('')[i])
                formatted += mask.split('')[i];
        }
    }

    return formatted;
}

document.querySelectorAll('[data-mask]').forEach(function (e) {
    function pattern(elem) {
        elem.setAttribute('pattern', '[+][(][0-9]{5}[)] [0-9]{3}-[0-9]{2}-[0-9]{2}')
    }

    function format(elem) {
        const val = doFormat(elem.value, elem.getAttribute('data-format'));
        elem.value = doFormat(elem.value, elem.getAttribute('data-format'), elem.getAttribute('data-mask'));

        if (elem.createTextRange) {
            var range = elem.createTextRange();
            range.move('character', val.length);
            range.select();
        } else if (elem.selectionStart) {
            // elem.focus();
            elem.setSelectionRange(val.length, val.length);
        }
    }

    e.addEventListener('keyup', function () {
        format(e);
    });
    e.addEventListener('keydown', function () {
        format(e);
    });
    format(e)
    pattern(e)
});
