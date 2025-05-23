"use strict";

axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

let app = Vue.createApp({
        
    delimiters: ['[[', ']]'],
       
    data(){return{      

        loading: true,   
        first_load_done: false,

        experiment: null,
        experiment_before_edit: null,

        cancel_modal: false,
        upload_collaborators_modal : null,

        collaborators_list_error : "",

        csv_collaborators_list : "",   //csv collaborators list

        //modal instances
        edit_experiment_modal:null,
    }},

    methods:{       
        
        do_first_load:function do_first_load(){
           
            //setup modals
            app.edit_experiment_modal = bootstrap.Modal.getOrCreateInstance(document.getElementById('edit_experiment_modal'), {keyboard: false});
            app.upload_collaborators_modal = bootstrap.Modal.getOrCreateInstance(document.getElementById('upload_collaborators_modal'), {keyboard: false});
            
            document.getElementById('edit_experiment_modal').addEventListener('hidden.bs.modal', app.hide_edit_experiment_modal);
            document.getElementById('upload_collaborators_modal').addEventListener('hidden.bs.modal', app.hide_send_collaborators_list);

            app.first_load_done = true;
        },

        clear_main_form_errors:function clear_main_form_errors(){
            for(let item in app.experiment)
            {
                let e = document.getElementById("id_errors_" + item);
                if(e) e.remove();
            }
        },

        //get experiment info from server
        get_experiment: function get_experiment(){
            axios.post('{{request.get_full_path}}', {
                        status:"get",                                                              
                })
                .then(function (response) {                                   
                    // app.institutions= response.data.institutions; 
                    app.experiment =  response.data.experiment;     
                   
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
        
        //show edit experiment modal
        show_edit_experiment: function show_edit_experiment(){
            app.experiment_before_edit = Object.assign({}, app.experiment);
            app.edit_experiment_modal.toggle(); //show modal
            app.cancel_modal=true;
            app.clear_main_form_errors();
        },

        //update experiment parameters
        send_update_experiment: function send_update_experiment(){

            app.cancel_modal=false;  
            
            axios.post('{{request.get_full_path}}', {
                    status :"update" ,                                
                    form_data : app.experiment,                                                            
                })
                .then(function (response) {     
                                                   
                    status=response.data.status;                               

                    app.clear_main_form_errors();

                    if(status=="success")
                    {                                 
                        app.experiment =  response.data.experiment;  
                        app.edit_experiment_modal.toggle(); //hide modal
                    }
                    else
                    {      
                        app.cancel_modal=true;                          
                        app.display_errors(response.data.errors);
                    }          
                 
                })
                .catch(function (error) {
                    console.log(error);
                    app.searching=false;
                });                        
        },

        //fire when edit experiment model hides, cancel action if nessicary
        hide_edit_experiment_modal:function hide_edit_experiment_modal(){
            if(app.cancel_modal)
            {
                Object.assign(app.experiment, app.experiment_before_edit);
                app.experiment_before_edit=null;
                app.cancel_experiment=false;
            }
        },

        /**
         * remove collaborator from session
         */
        send_remove_collaborator: function send_remove_collaborator(collaborator_id){

            axios.post('{{request.get_full_path}}', {
                status :"remove_collaborator" ,                                
                collaborator_id : collaborator_id,                                                            
            })
            .then(function (response) {     
                                               
                status=response.data.status;                               

                app.experiment = response.data.experiment;
                   
            })
            .catch(function (error) {
                console.log(error);
                app.searching=false;
            });   
        },

        /** show edit subject modal
        */
        show_upload_collaborators_list_modal : function show_upload_collaborators_list_modal (){
            app.clear_main_form_errors();
            app.cancel_modal=true;

            app.email_list_error = "";

            app.collaborators_list_error = "";

            app.upload_collaborators_modal.toggle();
        },

        /** hide edit subject modal
        */
        hide_send_collaborators_list: function hide_send_collaborators_list(){
            app.csv_collaborators_list = "";

            if(app.cancel_modal)
            {      
            
            }
        },

        /** send session update form   
        */
        send_add_collaborators: function send_add_collaborators(){
            axios.post('{{request.get_full_path}}', {
                status :"add_collaborators" ,                                
                csv_data : app.csv_collaborators_list,                                                            
            })
            .then(function (response) {     
                                               
                status=response.data.status;                               

                app.clear_main_form_errors();

                if(status=="success")
                {                                 
                    app.experiment =  response.data.experiment;  
                    app.upload_collaborators_modal.toggle(); //hide modal
                    app.csv_collaborators_list = "";
                    app.collaborators_list_error = "";
                }
                else
                {      
                    app.collaborators_list_error = response.data.errors_message;                        
                }          
             
            })
            .catch(function (error) {
                console.log(error);
                app.searching=false;
            });
        },

    },

    mounted(){
        Vue.nextTick(() => {
            app.get_experiment();
        });
    },                 

}).mount('#app');

