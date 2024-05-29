// loading animation
window.addEventListener('load', hideBackground);

function hideBackground() {
    var bh = document.querySelector('.loadingio-spinner-eclipse-2by998twmg8');  
    bh.classList.add('hid'); 
}
// loading animation ends ----------------------------


// add to cart 
$(document).ready(function () {
    $('.cartlogoandtext').click(function (e) { 

        value_of_quantity = $('#quantity').val();
        p_id = $('#p_id').val();
        $.ajax({
            type: "GET",
            url: "/add_to_cart/",
            data: {'quantity':value_of_quantity,'p_id':p_id},
            dataType: "json",
            success: function (data) {
                if (data.message == 'success'){
                    $('.popup').css({'opacity':'1','display':'block'});
                    gwt_cart_quantity();
                    setTimeout(function() {
                        $('.popup').css({'opacity':'0','display':'none'});
                    }, 2000);
                }
            }
        });
        
    });

});


// remove from cart
$(document).ready(function () {
    $('.butt').click(function (e) { 
        e.stopPropagation();  
        e.preventDefault();
        cart_id = $(this).data('cartid');
        // alert(cart_id);
        // alert($(this).parent().parent().parent().data('val'));
        cart_card = $(this).parent().parent().parent();
        cart_card.css({'transform':'scale(.1)','opacity':'0'});
        setTimeout(function(){cart_card.remove();},500);
        $.ajax({
            type: "GET",
            url: "/rem_from_cart/",
            data: {'cart_id': cart_id},
            dataType: "json",
            success: function (response) {
                if (response.total == '0'){
                    location.reload();
                }
                $('#disp_total_amount').text("Total amount = " + response.total);
                gwt_cart_quantity();
            }
        });
    });

});

// show cart quantity in navbar cart
$(document).ready(gwt_cart_quantity());

function gwt_cart_quantity(){
    $.ajax({
        type: "GET",
        url: "/get_total_quantity/",
        data: "data",
        dataType: "json",
        success: function (response) {
            console.log('asdas' + response.quantity);
            $('#cart_num').text('Cart ' + response.quantity);
        }
    });
}

$(document).ready(function() {
    var $logoutLink = $('#logout_link');
    var $logoutModal = $('#logoutModal');
    var $cancelLogout = $('#cancelLogout');
    var $modalBackdrop = $('.modal_backdrop');

    // Show modal when logout link is clicked
    $logoutLink.on('click', function(event) {
        event.preventDefault(); // Prevent the default behavior of the anchor tag
        $logoutModal.css('display', 'block');
        $modalBackdrop.css('display','block');
    });

    // Close modal when cancel button is clicked
    $cancelLogout.on('click', function() {
        $logoutModal.css('display', 'none');
        $modalBackdrop.css('display','none');
    });

    // Close modal when clicking outside the modal
    $modalBackdrop.on('click', function() {
        $logoutModal.css('display', 'none');
        $modalBackdrop.css('display','none');
    });

    // Prevent modal from closing when clicking inside the modal
    $logoutModal.on('click', function(event) {
        event.stopPropagation(); // Prevent event from bubbling up to modalBackdrop
    });
});






