/** @odoo-module **/

import { Component, useState, onWillStart } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { useService } from "@web/core/utils/hooks";
import { usePos } from "@point_of_sale/app/store/pos_hook";

export class SelectPreauthPopup extends Component {
    static template = "os_payment_pos.SelectPreauthPopup";
    static components = { Dialog };
    static props = {
        close: Function,
        customerId: Number,
        monerisPaymentMethodId: Object,
    };

    setup() {
        this.orm = useService("orm");
        this.pos = usePos();
        this.notification = useService("notification");
        this.ui = useState(useService("ui"));

        this.state = useState({
            preauthOrders: [],
            selectedOrder: null,
            loading: true,
        });

        onWillStart(async () => {
            await this.loadPreauthOrders();
        });
    }

    async loadPreauthOrders() {
        try {
            debugger
            const orders = await this.orm.searchRead(
                "moneris.pos.preauth",
                [
                    ["customer_id", "=", this.props.customerId],
                    ["status", "=", "confirmed"],
                    ["moneris_go_payment_method",'in',this.props.monerisPaymentMethodId.map(m => m.id)]
                ],
                ["name", "order_date", "order_id", "transaction_id",'moneris_go_payment_method', "total_amount", "status"]
            );
            this.state.preauthOrders = orders;
        } catch (err) {
            console.error(err);
            this.notification.add("Failed to load preauth orders", {type: "danger"});
        } finally {
            this.state.loading = false;
        }
    }

    selectOrder(order) {
        debugger
        this.state.selectedOrder = order;
    }

    async confirmSelection() {
        if (!this.state.selectedOrder) {
            this.notification.add("Please select a preauth order.", {type: "warning"});
            return;
        }


        const order = this.pos.get_order();
        if (order.get_due() < this.state.selectedOrder.total_amount) {
            this.notification.add("Authorized amount is greater than remaining amount.", {type: "warning"});
            return;
        }
        const matchedMethod = this.props.monerisPaymentMethodId.find(
        pm => pm.id === this.state.selectedOrder.moneris_go_payment_method[0]
        );

        if (!matchedMethod) {
            this.notification.add("No matching Moneris payment method found.", { type: "danger" });
            return;
        }
        try {
            this.state.loading = true; // Start loader
            debugger
            const args = [this.state.selectedOrder,matchedMethod.id,order.id, ...(this.props.extraArgs || [])];
            const res = await this.orm.call(
                "moneris.pos.preauth",          // model
                "moneris_preauth_complete_req",          // method
                args,                           // args
                {}                              // kwargs
            );

            console.log("RPC OK:", res);
            const response = JSON.parse(res);
            debugger
            if (response.errors_message) {
                return this.notification.add("Moneris GO Error: " + (response.errors_message), {
                    type: "danger",
                    sticky: true
                });
            }
            else if (response.error) {
                return this.notification.add("Moneris GO Error: " + (response.description), {
                    type: "danger",
                    sticky: true
                });
            }
            else{
                debugger
                order.add_paymentline(matchedMethod);
                order.get_selected_paymentline().set_amount(this.state.selectedOrder.total_amount);
                order.get_selected_paymentline().set_payment_status('done');
            }


            this.props.close();
        } catch (e) {
            console.error("RPC ERROR:", e);
            this.notification.add("Operation failed: " + (e?.message || e), {type: "danger"});
        } finally {
            this.state.loading = false; // Stop loader
        }


    }
}
