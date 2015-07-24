$(function() {
    var datetime_format = django.get_format('DATETIME_FORMAT');

    $("#comment_form").ajaxForm(function(comment) {
        var updated_at = new Date(comment.updated_at).format(datetime_format);
        $("#comment_form")[0].reset();
        $("#comment_list tbody").prepend($('<tr><td><pre>' + comment.message + '</pre><span>' + updated_at + '</span></td></tr>'));
        $.toaster({
            priority: 'info',
            message: 'Added a new comment.'
        });
    })
    $(".comment-delete-confirm").click(function() {
        var url = $(this).attr("href");
        var target = $(this).parent().parent();

        if ( confirm("Are you sure to delete the comment?") ) {
            $.ajax({
                url: url,
                method: "POST",
            }).done(function() {
                target.remove();
                $.toaster({
                    priority: 'danger',
                    message: 'Deleted a comment.'
                });
            }).fail(function() {
                $.toaster({
                    priority: 'danger',
                    message: 'Failed'
                });
            });
        }
        return false;
    });
});