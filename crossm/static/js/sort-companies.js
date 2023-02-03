const allCopmanies = document.querySelectorAll('.company')
let allCompainesName = []
let currentCompanyTitle
let isCompanyActive = false
let masonry



allCopmanies.forEach((e) => {
    allCompainesName.push(e.innerHTML)
})

const dashAllCompaniesName = allCompainesName.map((e) => "—&nbsp" + e)
allCopmanies.forEach((el, index) => {
    el.innerHTML = dashAllCompaniesName[index]
})

const allCopmaniesClick = allCopmanies.forEach((el) => {

    el.addEventListener('click', () => {
        document.querySelector('.pop-up').style.opacity = '0'
        document.querySelector('.pop-up').style.visibility = 'hidden'
        document.querySelector('.add-offer').style.color = '#000000'

        allCopmanies.forEach((el) => {
            el.classList.remove('company-active')
        })

        el.classList.toggle("company-active")
        currentCompanyTitle = el.innerHTML.slice(7)
        document.querySelector('.add-offer').href = `/offers/create/${el.id}`
        isCompanyActive = true
        let allCompanyCardTitle = document.querySelectorAll('.company-card-name')

        allCompanyCardTitle.forEach((el) => {
            el.closest('.company-card').style.display = 'block'
            

            if (el.innerHTML != currentCompanyTitle) {
                el.closest('.company-card').style.display = 'none'
            }
        })
        
    })
    

})

document.addEventListener('click', (e) => {

        masonry = new Masonry('.grid', {
        gutter: '.gutter-sizer',
        itemSelector: '.grid-item',
        columnWidth: '.grid-sizer',
        percentPosition: true,
        transitionDuration: '0.2s', 
      });
    
    
    if (!isCompanyActive) {
        
    
    const targetElement = e.target

        if (targetElement.classList.contains('add-offer') || targetElement.classList.contains('pop-up') || targetElement.classList.contains('pop-up-arrow') || targetElement.classList.contains('p-pop-up')) {
        document.querySelector('.pop-up').style.opacity = '1'
        document.querySelector('.pop-up').style.visibility = 'visible'
        document.querySelector('.add-offer').style.borderBottom = '3px solid transparent'
        }

        else {
        document.querySelector('.pop-up').style.opacity = '0'
        document.querySelector('.pop-up').style.visibility = 'hidden'
        document.querySelector('.add-offer').style.borderBottom = '3px solid #807EFD'
        }
    }
})

window.onload = () => {
    masonry = new Masonry('.grid', {
    gutter: '.gutter-sizer',
    itemSelector: '.grid-item',
    columnWidth: '.grid-sizer',
    percentPosition: true,
    transitionDuration: '0.2s', 
  });
};