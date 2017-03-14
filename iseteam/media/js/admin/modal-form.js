$('body').ready(function(){
    var view = $(this).find('.modal-form-view');
    $(view).on('loaded.bs.modal', function(){
        set_view(this);
    });
    set_view(view);
});

function set_view(view){
    $(view).each(function(){
        var form = $(this).find('form');
        var submit_buttom = $(form).find('button[type="submit"]');
        var input_fields = $(form).find('input').not('[type="hidden"]')
        $(input_fields).focusin(function(){
            setValidStates(this)
        });
        var field_labels = $(form).find('label');
        $(submit_buttom).click(function(e){
            e.preventDefault();
            var valid = true;
            var error_msg = "";
            // Verify required fields are properly filled
            var required_fields = $(input_fields).filter('[required]');
            var required_fields_unfilled = $(required_fields).filter(function(){
                if($(this).attr('type') === 'number'){
                    return !$.isNumeric($(this).val())
                }
                return $(this).val().trim() === "";
            });
            $(required_fields_unfilled).each(function(){
                valid = false;
                var field_label = $(field_labels).filter('[for="' + $(this).attr('id') + '"]')
                var field_name = $(field_label).text();
                error_msg += "\nField " + field_name + " is required."
                setValidStates(this, "error")
            });
            if(valid){
                var modal_content = $(view).find('.modal-content');
                var data = {};
                $(form).find(':input').each(function(){
                    var key = $(this).attr('name');
                    var value = $(this).val();
                    data[key] = value;
                });
                var url = $(form).attr('action');

                var request = $.post(url, data)
                request.done(function(data){
                    if($(form).data('reload_when_submit_success')){
                        location.reload();
                    }
                });
                request.always(function(data){

                });
            }else{
                alert("There is an error with the form.\n" + error_msg + "\n\nPlease fix it and try again.")
            }
        });
    });
}

function setValidStates(field, state){
    var container = $(field).parent()
    $(container).removeClass('has-success');
    $(container).removeClass('has-warning');
    $(container).removeClass('has-error');
    $(container).removeClass('has-feedback');
    $(container).find('span.form-control-feedback').remove();
    if(state == 'error'){
        var containerClassName = 'has-error';
        var feedbackClassName = 'glyphicon-ok';
    }else if(state == 'warning'){
        var containerClassName = 'has-warning';
        var feedbackClassName = 'glyphicon-warning-sign';
    }else if(state == 'success'){
        var containerClassName = 'has-success';
        var feedbackClassName = 'glyphicon-remove';
    }else{
        return false
    }
    $(container).addClass(containerClassName);
    $(container).addClass('has-feedback');
    var feedback = $('<span></span>');
    $(feedback).addClass('glyphicon');
    $(feedback).addClass('form-control-feedback');
    $(feedback).attr('aria-hidden', true);
    $(feedback).addClass(feedbackClassName);
    $(container).append(feedback)
}