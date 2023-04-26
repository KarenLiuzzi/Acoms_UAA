// IIFE PATTERN 
;(function(){
    const modal = new bootstrap.Modal(document.getElementById("modal"))

    //const modal2 = document.getElementById("modal");

    htmx.on("htmx:afterSwap", (e) => {
      // Response targeting #dialog => show the modal
      if (e.detail.target.id == "dialog") {

        
        // $('#modal').modal({
        //   keyboard: false, backdrop:'static'
        // })

        // modal({backdrop:'static', keyboard:false, focus: true})
        modal.show()
        

        // document.getElementById("modal")

        // agregado ver si hay que sacar
        
        // modal.modal({backdrop: true, keyboard: false, show: true});
        // modal.data('bs.modal').options.backdrop = 'static';
        // modal.data('bs.modal')._config.backdrop = 'static';
      }
    })

    // Obtenga el modal
    //var modal = document.getElementById("miModal");

    // Cuando se envía el formulario, cierre el modal
    //document.querySelector("form").addEventListener("submit", function() {
    //  modal.style.display = "none";
    //});

    htmx.on("htmx:beforeSwap", (e) => {
      // console.log(e.detail.xhr.response)
      // console.log(e.detail.target.id)
        // Empty response targeting #dialog => hide the modal
        //if (e.detail.target.id == "dialog" && !e.detail.xhr.response) {
          if (e.detail.target.id == "dialog" && !e.detail.xhr.response) {
          modal.hide()
          e.detail.shouldSwap = false
          //agregado ver si sacar 
          // modal.data('bs.modal',null);

        }
      })

      htmx.on("hidden.bs.modal", () => {
        document.getElementById("dialog").innerHTML = ""
      })
      
})()

