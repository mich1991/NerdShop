const element = document.querySelector('#toast')
    const button = document.querySelector('#close-button')
    const closeAlert = () => {
        element.style.opacity = 0
        setTimeout(() => {
            element.remove()
        }, 500)
    }
    button.addEventListener('click', () => {
        closeAlert()
    })
    setTimeout(() => {
        closeAlert()
    }, 5000)