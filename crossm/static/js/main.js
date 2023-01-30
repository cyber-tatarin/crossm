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