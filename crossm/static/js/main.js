const renderSelect = () =>{
    const elements = document.querySelectorAll('.js-choice');
    elements.forEach(el =>{
        const choices = new Choices(el, {
            itemSelectText : "",
            noResultsText: 'Не найдено',
        })
    })
}

renderSelect()

window.onload = () => {
    document.querySelector('.Test').style.opacity = '0';
    document.querySelector('.Test').style.visibility = 'hidden'
    document.querySelector('.Test').style.zIndex = '-10'
}