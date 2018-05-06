odoo.define('payment_checkout.checkout', function(require) {
    "use strict";

    var ajax = require('web.ajax');
    var core = require('web.core');
    var _t = core._t;
    var Qweb = core.qweb;
    ajax.loadXML('/payment_checkout/static/src/xml/checkout_templates.xml', Qweb);

    // The following currencies are integer only.
    var int_currencies = [
        'BYR', 'BIF', 'DJF', 'GNF', 'ISK', 'KMF', 'XAF', 'CLF', 
        'XPF', 'JPY', 'PYG', 'RWF', 'KRW', 'VUV', 'VND', 'XOF'
    ];

    // The following currencies are Divided only.
    var div_currencies = ['BHD', 'LYD', 'JOD', 'KWD', 'OMR', 'TND']

    if ($.blockUI) {
        // to show spin
        $.blockUI.defaults.baseZ = 2147483647; 
        $.blockUI.defaults.css.border = '0';
        $.blockUI.defaults.css["background-color"] = '';
        $.blockUI.defaults.overlayCSS["opacity"] = '0.9';
    }

    function getCheckout(data){
    	var tx_ref = $(data).find('input[name="order_no"]').attr('value');
    	var amount = parseFloat($("input[name='amount']").val() || '0.0');
		var currency = $("input[name='currency']").val();
		if (!_.contains(int_currencies, currency)) {
            amount = amount*100;
        }
		if (_.contains(div_currencies, currency)) {
            amount = amount * 1000;
        }
		Checkout.configure({
	        payButtonSelector: '.pay_checkout' || '#pay_checkout',
	        publicKey: $("input[name='publishable_key']").val(),
	        customerEmail: $("input[name='email']").val(),
	        value: amount,
	        currency: currency,
	        paymentMode: 'cards',
	        debugMode: true,
	        cardFormMode: 'cardTokenisation',
	        cardTokenised: function (event) {
	        	if ($.blockUI) {
                    var msg = _t("Just one more second, confirming your payment...");
                    $.blockUI({
                        'message': '<h2 class="text-white"><img src="/web/static/src/img/spin.png" class="fa-pulse"/>' +
                                '    <br />' + msg +
                         '</h2>'
                    });
                }
	            var cardtoken = event.data.cardToken;
	            ajax.jsonRpc("/payment/checkout/create_charge", 'call', {
	                tx_url : $("input[name='tx_url']").val(),
	                cardtoken : cardtoken,
	                tx_ref: tx_ref,
	                secret_key: $("input[name='secret_key']").val(),
	                customerName: $("input[name='customerName']").val(),
	                email: $("input[name='email']").val(),
	                amount: amount,
	                currency : currency,
	                return_url : $("input[name='return_url']").val(),
	                billingDetails : $("input[name='billingDetails']").val(),
	            }).always(function(){
                    if ($.blockUI) {
                        $.unblockUI();
                    }
	            }).done(function(data){
	            	window.location.href = data;
	            }).fail(function(){
	            	var msg = arguments && arguments[1] && arguments[1].data && arguments[1].data.arguments && arguments[1].data.arguments[0];
                    var wizard = $(Qweb.render('checkout_error', {'msg': msg || _t('Payment error')}));
                    wizard.appendTo($('body')).modal({'keyboard': true});
	            });
	        }
	    });
		Checkout.open();
	}
	$('#pay_checkout').on('click', function(e) {
		var payment_form = $('.o_payment_form');
		var acquirer = $(e.currentTarget).parents('div.oe_sale_acquirer_button').first();
        var acquirer_id = acquirer.data('id');
		if (! acquirer_id) {
            return false;
        }
        var so_token = $("input[name='token']").val();
        var so_id = $("input[name='return_url']").val().match(/quote\/([0-9]+)/) || undefined;
        if (so_id) {
            so_id = parseInt(so_id);
        }
        e.preventDefault();
        if ($('.o_website_payment').length !== 0) {
            ajax.jsonRpc('/website_payment/transaction', 'call', {
		        amount: amount,
		        currency_id: currency,
		        acquirer_id: acquirer_id
         })
        }else{
			ajax.jsonRpc('/shop/payment/transaction/' + acquirer_id, 'call', {
	            so_id: so_id,
	            so_token: so_token
	        }, {'async': false}).then(function (data) {
	            var newForm = document.createElement('form');
	            newForm.setAttribute("provider", 'checkout');
	            newForm.hidden = true; // hide it
	            newForm.innerHTML = data;
	            getCheckout(newForm);
	        });
        }
	});
});

