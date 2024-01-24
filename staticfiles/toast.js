// IIFE PATTERN 
;(function(){
    const toastElement = document.getElementById("toast")
    const toastBody = document.getElementById("toast-body")
    
    const toast = new bootstrap.Toast(toastElement, { delay: 2000 })
    
    htmx.on("showMessage", (e) => {
      console.log('entro en notificaicon ')
      toastBody.innerText = e.detail.value
      toast.show()
    })
    
    })()