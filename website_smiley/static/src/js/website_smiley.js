odoo.define('website_smiley.smiley_rating', function (require) {
"use strict";

    var ajax = require('web.ajax');

    $(document).ready(function(){
        $('.o_livechat_rating img').on('click', function (ev) {
        	var rating = parseInt($(ev.currentTarget).data('value'));
    		var self = this;
            var args = {
                uuid: 1,
                rate: rating,
                reason : 'Reason'
            };
            ajax.jsonRpc("/smiley/rating", 'call', args).then(function (data) {
            	$('.o_livechat_rating img').addClass('hidden');
            	$('.o_livechat_smiley .alert').removeClass('hidden');
            });
    	});
    });
});
