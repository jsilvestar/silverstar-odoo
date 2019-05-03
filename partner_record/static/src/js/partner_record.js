odoo.define('partner_record.partner', function(require) {
"use strict";

var ActionManager = require('web.ActionManager');
var core = require('web.core');
var Widget = require('web.Widget');
var Model = require('web.Model');
var Partners = new Model('res.partner')

var QWeb = core.qweb;
var _t = core._t;

var PartnerRecord = Widget.extend({

	events: {
        'click .o_edit_button': 'edit_partner_line',
        'click .o_save_button': 'save_partner_line',
        'click .o_action_partner': 'on_partner_clicked',
    },

    start: function() {
    	var sup = this._super();
    	var self = this;
    	self.render();
    },

    /*render template passing partner values */
    render: function(){
    	var self = this;
    	var partners = Partners.query(['name', 'image'])
    	.filter([['active', '=', true]])
    	.all().then(function(result) {
    		self.$el.append(QWeb.render("PartnerTemplate", {partners: result}));
    	});
    },

    /* edit button */
    edit_partner_line: function(event) {
        var self = this;
        var span = $(event.currentTarget).parent().parent().find('span')
        console.log(span)
        var partner_id = $(event.currentTarget).data('edit-id');
        self.$(span).replaceWith('<input type="text" value="'+ span.text() +'" t-att-value="'+ span.text() +'" class="oe_form_field" t-att-data-partner_id="'+partner_id+'"/>')
        self.$(".o_edit_button[data-edit-id='"+ partner_id +"']").addClass("hidden");
        self.$(".o_save_button[data-save-id='"+ partner_id +"']").removeClass("hidden");
    },

    /* save button */
    save_partner_line: function(event) {
        var self = this;
        var partner_id = $(event.currentTarget).data('save-id');
        var name = $(event.currentTarget).parent().parent().find('input').val();
//        var name = self.$("input[data-partner_id='"+ partner_id +"']").val();
        console.log(name)
        if (name === "") return;

        /*Calling write function in python*/
        return Partners
	    .call('write', [[partner_id], {'name': name}])
	    .done(function () {
            self.$(".o_edit_button[data-edit-id='" +partner_id+ "']").removeClass("hidden");
            self.$(".o_save_button[data-save-id='" +partner_id+ "']").addClass('hidden');
            window.location.reload();
        });
    },

   /* open partner record*/
    on_partner_clicked: function(event){
        event.preventDefault();
        var partner_id = $(event.currentTarget).data('partner_id');
        this.do_action({
            name: "Customers",
            res_model: 'res.partner',
            views: [
                    [false, 'form'],
                   ],
            type: 'ir.actions.act_window',
            view_type: "form",
            view_mode: "form",
            res_id: partner_id,
            target: 'new',
        });
    },

});
core.action_registry.add('partner_record', PartnerRecord);
});
