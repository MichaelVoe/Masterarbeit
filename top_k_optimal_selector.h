#ifndef SYMBOLIC_TOP_K_OPTIMAL_SELECTOR_H
#define SYMBOLIC_TOP_K_OPTIMAL_SELECTOR_H

#include "plan_database.h"

namespace symbolic {

    class TopKSelectorOptimal : public PlanDataBase {
    public:
        TopKSelectorOptimal(const options::Options &opts);
        
        ~TopKSelectorOptimal() {};
        
        void add_plan(const Plan& plan) override;

        virtual bool found_enough_plans() const override {
            return num_accepted_plans >= num_desired_plans || min_plan_cost == -1;
        }
        
        std::string tag() const override {
            return "Optimal-Top-K";
        }

    protected:
        int min_plan_cost;

    };
    
}


#endif /* SYMBOLIC_TOP_K_OPTIMAL_SELECTOR_H */
