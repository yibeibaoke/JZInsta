
function error_cb(error) {
    console.log(error);
}
/*
 *
 *    Follow/Unfollow
 *
 */

function follow_user(success_cb, error_cb, type) {
    // var follow_profile_pk = $(this).closest('.follow__card').attr('id')
    //                       || $(this).attr('id');
    var follow_user_pk = $(this).attr('id');
    console.log(follow_user_pk);
  
    $.ajax({
      type: "POST",
      url: '/togglefollow',
      data: {
        follow_user_pk: follow_user_pk,
        type: type
      },
      success: function(data) { success_cb(data); },
      error: function(error) { error_cb(error); }
    });
  }
  
function update_follow_view(data) {
    console.log('calling update_follow_view');
    console.log('data',data);
    var $button = $('.follow-toggle__container .btn');
    $button.addClass('unfollow-user').removeClass('follow-user');
    $button.text('Unfollow');
}

function update_unfollow_view(data) {
    console.log('calling update_unfollow_view');
    console.log('data',data);
    var $button = $('.follow-toggle__container .btn');
    $button.addClass('follow-user').removeClass('unfollow-user');
    $button.text('Follow');
}


$('.follow-toggle__container').on('click', '.follow-user', function() {
    follow_user.call(this, update_follow_view, error_cb, 'follow');
});

$('.follow-toggle__container').on('click', '.unfollow-user', function() {
    follow_user.call(this, update_unfollow_view, error_cb, 'unfollow');
});