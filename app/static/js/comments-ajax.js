/**
 * WordPress jQuery-Ajax-Comments v1.3 by Willin Kan.
 * URI: http://kan.willin.org/?p=1271
 * for WP3.5+ | modified version URI: http://zww.me/wordpress3-5-willin-ajax-comment.z-turn
 */
var i = 0, got = -1, len = document.getElementsByTagName('script').length;
while (i <= len && got == -1) {
    var js_url = document.getElementsByTagName('script')[i].src,
        got = js_url.indexOf('comments-ajax.js');
    i++;
}
var edit_mode = '1', // 再編輯模式 ( '1'=開; '0'=不開 )

    ajax_php_url = js_url.replace('-ajax.js', '-ajax.php'),
    wp_url = js_url.substr(0, js_url.indexOf('wp-content')),
    pic_sb = wp_url + 'wp-admin/images/wpspin_dark.gif', // 提交 icon
    pic_no = wp_url + 'wp-admin/images/no.png',      // 錯誤 icon
    pic_ys = wp_url + 'wp-admin/images/yes.png',     // 成功 icon
    txt1 = '<div id="loading"></div>',
    txt2 = '<div id="error">#</div>',
    txt3 = '"> <div id="edita">您的评论已经提交成功',
    edt1 = ',如有异议刷新前你可以再次 <a rel="nofollow" class="comment-reply-link_a" href="#edit" onclick=\'return addComment.moveForm("',
    edt2 = ')\'>[修改评论]</a></div> ',
    cancel_edit = '[取消]',
    edit, num = 1, comm_array = [];
comm_array.push('');

jQuery(document).ready(function ($) {
    $comments = $('#comments-title'); // 評論數的 ID
    $cancel = $('#cancel-comment-reply-link');
    cancel_text = $cancel.text();
    $submit = $('#commentform #submit');
    $submit.attr('disabled', false);
    $('#comment').after(txt1 + txt2);
    $('#loading').hide();
    $('#error').hide();
    $body = (window.opera) ? (document.compatMode == "CSS1Compat" ? $('html') : $('body')) : $('html,body');

    /** submit */
    $('#commentform').submit(function () {
        $('#loading').fadeIn();
        $submit.attr('disabled', true).fadeTo('slow', 0.5);
        if (edit) $('#comment').after('<input type="text" name="edit_id" id="edit_id" value="' + edit + '" style="display:none;" />');
        var nickname = $('#author').val();
        var email = $('#email').val();
        var content = $('#comment').val();
        var csrftoken = $('input[name=csrf_token]').val();
        var emailReg = /[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}/
        if (!emailReg.test(email)) {
            alert(" 请输入有效的邮箱");
            return false;
        }
        /** Ajax */
        $.ajax({
            url: '/addcomment',
            data: $(this).serialize(),
            //data:{nick_name:nickname, email:email, content:content},
            type: $(this).attr('method'),
            //dataType: 'json',
            beforeSend: function (xhr, settings) {
                if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken)
                }
            },
            error: function (request) {
                $('#loading').slideUp();
                $('#error').fadeIn(500).html('<span class="submit-er"></span> ' + request.responseText);
                setTimeout(function () {
                    $submit.attr('disabled', false).fadeTo('slow', 1);
                    $('#error').slideUp();
                }, 3000);
            },

            success: function (data) {
                if (data.code == 1) {
                    $('#loading').hide();
                    comm_array.push($('#comment').val());
                    $('textarea').each(function () {
                        this.value = ''
                    });
                    var t = addComment, cancel = t.I('cancel-comment-reply-link'), temp = t.I('wp-temp-form-div'),
                        respond = t.I(t.respondId), post = t.I('comment_post_ID').value,
                        parent = t.I('comment_parent').value;

// comments
                    if (!edit && $comments.length) {
                        n = parseInt($comments.text().match(/\d+/));
                        $comments.text($comments.text().replace(n, n + 1));
                    }

// show comment
                    new_htm = '" id="new_comm_' + num + '"></';
                    new_htm = (parent == '0') ? ('\n<ol style="clear:both;" class="commentwrap' + new_htm + 'ol>') : ('\n<ul class="children' + new_htm + 'ul>');

                    ok_htm = '\n<span id="success_' + num + txt3;
                    if (edit_mode == '1') {
                        div_ = (document.body.innerHTML.indexOf('div-comment-') == -1) ? '' : ((document.body.innerHTML.indexOf('li-comment-') == -1) ? 'div-' : '');
                        ok_htm = ok_htm.concat(edt1, div_, 'comment-', parent, '", "', parent, '", "respond", "', post, '", ', num, edt2);
                    }
                    ok_htm += ' </span><span></span>\n';

                    $('#respond').before(new_htm);
                    $('#new_comm_' + num).hide().append(data);
                    $('#new_comm_' + num + ' li').append(ok_htm);
                    $('#new_comm_' + num).fadeIn(600);

                    /*                 $body.animate({scrollTop: $('#new_comm_' + num).offset().top - 200}, 900);
                     */
                    countdown();
                    num++;
                    edit = '';
                    $('*').remove('#edit_id');
                    cancel.style.display = 'none';
                    cancel.onclick = null;
                    t.I('comment_parent').value = '0';
                    if (temp && respond) {
                        temp.parentNode.insertBefore(respond, temp);
                        temp.parentNode.removeChild(temp)
                    }
                    var image = data.head_image;
                    var strtime = data.strtime;
                    // 评论内容追加到输入框下
                    var h = '<li class="comment odd alt thread-odd thread-alt depth-1" id="li-comment-">';
                    h += '<div id="comment-949" class="comment_body contents">';
                    h += '<div class="profile">';
                    h += '<a href=""><img src="static/user_images/' + image + '" class="gravatar" alt="' + nickname + '"></a>';
                    h += '</div>';
                    h += '<div class="main shadow">';
                    h += '<div class="commentinfo">';
                    h += '<section class="commeta">';
                    h += '<div class="shang">';
                    h += '<h4 class="author"><a href="" target="_blank"><img src="static/user_images/' + image + '" class="gravatarsmall" alt="' + nickname + '">' + nickname + '</a></h4>';
                    h += '</div>';
                    h += '</section>';
                    h += '</div>';
                    h += '<div class="body">';
                    h += '<p>' + content + '</p>';
                    h += '</div>';
                    h += '<div class="xia info">';
                    h += '<span><time datetime="' + strtime + '">' + strtime + '</time></span>';
                    h += '</div>';
                    h += '</div>';
                    h += '</div>';
                    h += '</li>';
                    $('#load_comment ul').prepend(h);
                } else {
                    alert(data.msg);
                    window.location.reload();
                }
            }
        }); // end Ajax
        return false;
    }); // end submit

    /** comment-reply.dev.js */
    addComment = {
        moveForm: function (commId, parentId, respondId, postId, num) {
            var t = this, div, comm = t.I(commId), respond = t.I(respondId), cancel = t.I('cancel-comment-reply-link'),
                parent = t.I('comment_parent'), post = t.I('comment_post_ID');
            if (edit) exit_prev_edit();
            num ? (
                t.I('comment').value = comm_array[num],
                    edit = t.I('new_comm_' + num).innerHTML.match(/(comment-)(\d+)/)[2],
                    $new_sucs = $('#success_' + num), $new_sucs.hide(),
                    $new_comm = $('#new_comm_' + num), $new_comm.hide(),
                    $cancel.text(cancel_edit)
            ) : $cancel.text(cancel_text);

            t.respondId = respondId;
            postId = postId || false;

            if (!t.I('wp-temp-form-div')) {
                div = document.createElement('div');
                div.id = 'wp-temp-form-div';
                div.style.display = 'none';
                respond.parentNode.insertBefore(div, respond)
            }

            !comm ? (
                temp = t.I('wp-temp-form-div'),
                    t.I('comment_parent').value = '0',
                    temp.parentNode.insertBefore(respond, temp),
                    temp.parentNode.removeChild(temp)
            ) : comm.parentNode.insertBefore(respond, comm.nextSibling);

            /*             $body.animate({scrollTop: $('#respond').offset().top - 180}, 400);
             */
            if (post && postId) post.value = postId;
            parent.value = parentId;
            cancel.style.display = '';

            cancel.onclick = function () {
                if (edit) exit_prev_edit();
                var t = addComment, temp = t.I('wp-temp-form-div'), respond = t.I(t.respondId);

                t.I('comment_parent').value = '0';
                if (temp && respond) {
                    temp.parentNode.insertBefore(respond, temp);
                    temp.parentNode.removeChild(temp);
                }
                this.style.display = 'none';
                this.onclick = null;
                return false;
            };

            try {
                t.I('comment').focus();
            }
            catch (e) {
            }

            return false;
        },

        I: function (e) {
            return document.getElementById(e);
        }
    }; // end addComment

    function exit_prev_edit() {
        $new_comm.show();
        $new_sucs.show();
        $('textarea').each(function () {
            this.value = ''
        });
        edit = '';
    }

    var wait = 15, submit_val = $submit.val();

    function countdown() {
        if (wait > 0) {
            $submit.val(wait);
            wait--;
            setTimeout(countdown, 1000);
        } else {
            $submit.val(submit_val).attr('disabled', false).fadeTo('slow', 1);
            wait = 15;
        }
    }

});// end jQ