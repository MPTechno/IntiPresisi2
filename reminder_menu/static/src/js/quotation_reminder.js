odoo.define('reminder_menu.reminder_menu', function (require) {
    "use strict";

var bus = require('bus.bus').bus;
var core = require('web.core');
var Model = require('web.Model');
var CalendarView = require('web_calendar.CalendarView');
var data = require('web.data');
var Dialog = require('web.Dialog');
var SystrayMenu = require('web.SystrayMenu');
var WebClient = require('web.WebClient');
var weblient = require('web.web_client');
var widgets = require('web_calendar.widgets');
var Widget = require('web.Widget');
var UserMenu = require('web.UserMenu');
var Menu = require('web.Menu');
var _t = core._t;
var _lt = core._lt;
var QWeb = core.qweb;


    var QuotationReminder = Widget.extend({
        sequence: 100, // force it to be the left-most item in the systray to prevent flickering as it is not displayed in all apps
        template: "QuotationReminder",
        events: {
            "click": "on_menu_clicked",
        },
        init: function(parent) {
            this._super(parent);
        },
        start: function() {
            var self = this;
            var waiting_order = [];
            (new Model('sale.order')).query().all().then(function(order) {
                _.each(order, function(user) {
                    if (user.state == 'sent'){
                        waiting_order.push(user);
                    }
                });
                var total_count = waiting_order.length;
                $('.o_reminder_counter').text(total_count);
                var widget = $('.o_reminder_dropdown_channels', this.$el).html(QWeb.render('reminder_order',{
                    order: waiting_order,
                }));
            });
        },
        on_menu_clicked: function(menu_id) {
            var self = this;
            console.log('Menu Clicked...')
            $('.recorddata').click(function(){
                if ( $(this).attr('id') ){
                    self.open_ui($(this).attr('id'));
                }
            });
        },
        open_ui: function(sale_id){
            var self = this;
            console.log('self....',this);
            if (sale_id) {
                var action = {
                    type: 'ir.actions.act_window',
                    res_model: 'sale.order',
                    views: [[false, "form"]],
                    res_id: parseInt(sale_id),
                };
                self.do_action(action,{clear_breadcrumbs: true});
            }
        },
    });

    SystrayMenu.Items.push(QuotationReminder);

    return {
        QuotationReminder: QuotationReminder,
    };

});