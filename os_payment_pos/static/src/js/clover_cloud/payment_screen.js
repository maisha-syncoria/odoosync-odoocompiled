import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { patch } from "@web/core/utils/patch";
import { onMounted } from "@odoo/owl";
//
// patch(PaymentScreen.prototype, {
//      async sendForceDone(line) {
//         debugger
//         if (line.payment_method_id.use_payment_terminal == "clover_cloud") {
//           return Promise.resolve();
//         }
//
//         return  super.sendForceDone(...arguments);
//     },
// });