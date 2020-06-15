#include "top_k_optimal_selector.h"

#include "../../option_parser.h"

namespace symbolic {

    TopKSelectorOptimal::TopKSelectorOptimal(const options::Options &opts) :
    PlanDataBase(opts), min_plan_cost(std::numeric_limits<int>::max()) {
        PlanDataBase::anytime_completness = true;
    }

    void TopKSelectorOptimal::add_plan(const Plan& plan) {
        int plan_cost = 0;
        for (auto& op : plan) {
            plan_cost += sym_vars->get_state_registry()->get_task_proxy().get_operators()[op].get_cost();
        }

        if (!has_accepted_plan(plan) && plan_cost <= min_plan_cost) {
            save_accepted_plan(plan);
        }
        min_plan_cost = std::min(min_plan_cost, plan_cost);

        if (plan_cost > min_plan_cost) {
            min_plan_cost = -1;
        }
    }

    static std::shared_ptr<PlanDataBase> _parse(OptionParser &parser) {
        PlanDataBase::add_options_to_parser(parser);

        Options opts = parser.parse();
        if (parser.dry_run())
            return nullptr;
        return std::make_shared<TopKSelectorOptimal>(opts);
    }

    static Plugin<PlanDataBase> _plugin("top_k_optimal", _parse);

}
