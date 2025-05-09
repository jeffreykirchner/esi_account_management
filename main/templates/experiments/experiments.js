"use strict";

axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

let app = Vue.createApp({
        
    delimiters: ['[[', ']]'],
       
    data(){return{      

        loading: true,   
        first_load_done: false,

        experiments: null,
        managed_experiments: null,
    }},

    methods:{       
        
        do_first_load:function do_first_load(){           
            //setup modals           
            app.first_load_done = true;
            app.loading = false;
        },

        clear_main_form_errors:function clear_main_form_errors(){
            for(let item in app.experiment)
            {
                let e = document.getElementById("id_errors_" + item);
                if(e) e.remove();
            }
        },

        //get experiment info from server
        get_experiments: function get_experiment(){
            axios.post('{{request.get_full_path}}', {
                        status:"get",                                                              
                })
                .then(function (response) {                                   
                    // app.institutions= response.data.institutions; 
                    app.experiments = response.data.experiments;     
                    app.managed_experiments = response.data.managed_experiments;
                   
                    if(!app.first_load)
                    {   
                        Vue.nextTick(() => {
                            app.do_first_load();
                        });
                        // setTimeout(app.do_first_load, 250);
                        app.first_load = true;
                    }
                })
                .catch(function (error) {
                    console.log(error);
                    //app.searching=false;                                                              
                });                        
        },

        {% if user.is_superuser %}
        //add new experiment
        add_experiment: function add_experiment(){
            app.loading = true;
            axios.post('{{request.get_full_path}}', {
                        status:"add",                                                              
                })
                .then(function (response) {                                   
                    // app.institutions= response.data.institutions; 
                    app.experiments = response.data.experiments;     
                    app.managed_experiments = response.data.managed_experiments;
                    app.loading = false;
                })
                .catch(function (error) {
                    console.log(error);
                    //app.searching=false;                                                              
                });                        
        },

        //delete experiment
        delete_experiment: function delete_experiment(experiment_id){
            //confirm delete
            if(!confirm("Are you sure you want to delete this experiment?")) return;
            
            app.loading = true;
            axios.post('{{request.get_full_path}}', {
                        status:"delete",
                        experiment_id:experiment_id,
                })
                .then(function (response) {
                    app.experiments = response.data.experiments;
                    app.managed_experiments = response.data.managed_experiments;
                    app.loading = false;
                })
                .catch(function (error) {
                    console.log(error);
                    //app.searching=false;
                });
        },
        {%endif%}

        //display form errors
        display_errors: function display_errors(errors){
            for(let e in errors)
            {
                let str='<span id=id_errors_'+ e +' class="text-danger">';
                
                for(let i in errors[e])
                {
                    str +=errors[e][i] + '<br>';
                }

                str+='</span>';

                document.getElementById("div_id_" + e).insertAdjacentHTML('beforeend', str);

                document.getElementById("div_id_" + e).scrollIntoView();
                
            }
        },
        
        /** clear form error messages
        */
        clear_main_form_errors: function clear_main_form_errors(){
            
            for(let item in app.experiment)
            {
                let e = document.getElementById("id_errors_" + item);
                if(e) e.remove();
            }
        },

    },

    mounted(){
        Vue.nextTick(() => {
            app.get_experiments();
        });
    },                 

}).mount('#app');

