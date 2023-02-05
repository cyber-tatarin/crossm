window.onload = () => {
    masonry = new Masonry('.grid', {
        gutter: '.gutter-sizer',
        itemSelector: '.grid-item',
        columnWidth: '.grid-sizer',
        percentPosition: true,
        transitionDuration: '0.2s', 
      });
    document.querySelector('.Test').style.opacity = '0';
    document.querySelector('.Test').style.visibility = 'hidden'
    document.querySelector('.Test').style.zIndex = '-10'
}

const renderSelect = () => {
    const elements = document.querySelectorAll('.js-choice');
    elements.forEach(el =>{
        const choices = new Choices(el, {
            itemSelectText : "",
            noResultsText: 'Не найдено',
        })
    })
}

renderSelect()


const sortButton = document.getElementById('sort-button')
sortButton.addEventListener('click', (btn) => {

    let couponCountOt = document.getElementById('coupon-count-ot')
    let couponCountDo = document.getElementById('coupon-count-do')

    let retailPriceOt = document.getElementById('retail-price-ot')
    let retailPriceDo = document.getElementById('retail-price-do')

    let couponPriceOt = document.getElementById('coupon-price-ot')
    let couponPriceDo = document.getElementById('coupon-price-do')

    couponCountOt = couponCountOt.value ? (couponCountOt.value) : (couponCountOt.placeholder);
    couponCountDo = couponCountDo.value ? (couponCountDo.value) : (couponCountDo.placeholder);

    retailPriceOt = retailPriceOt.value ? (retailPriceOt.value) : (retailPriceOt.placeholder);
    retailPriceDo = retailPriceDo.value ? (retailPriceDo.value) : (retailPriceDo.placeholder);

    couponPriceOt = couponPriceOt.value ? (couponPriceOt.value) : (couponPriceOt.placeholder);
    couponPriceDo = couponPriceDo.value ? (couponPriceDo.value) : (couponPriceDo.placeholder);

    console.log(couponCountOt, couponCountDo, retailPriceOt, retailPriceDo, couponPriceOt, couponPriceDo)

    const checkbox = document.getElementById('phone')

    // console.log(couponCountOt.placeholder || couponCountOt.value)

    const choices = document.querySelectorAll('option')
        
    let nisha = choices[0].innerHTML;
    let valuta = choices[1].innerHTML;
    let country = choices[2].innerHTML
        
    const allCopmanies = document.querySelectorAll('.company-card')

    allCopmanies.forEach((el) => {

        el.style.display = 'block';
        // console.log(couponCountOt.placeholder)
        

        // let rescouponCountOt;
        // if (couponCountOt.value === '') {
        //     rescouponCountOt = couponCountOt.placeholder
        // }
        // else {
        //     rescouponCountOt = couponCountOt.value
        // }

        // if(couponCountOt.value === '') couponCountOt = couponCountOt.placeholder else 



        // const currentCompanyTitle = el.querySelector('.company-card-name').innerHTML;
        const currentCompanyNisha = el.querySelector('.nisha').innerHTML;
        // const currentCompanyYslyga = el.querySelector('.usluga').innerHTML;
        const currentCompanyCouponCount = el.querySelector('.coupon-count').innerHTML;
        const currentCompanyCouponPrice = el.querySelector('.coupon-price').innerHTML;
        const currentCompanyRetailPrice = el.querySelector('.retail-price').innerHTML;
        const currentCompanyPhone = el.querySelector('.contacts-phone').innerHTML

        let resCouponCount = currentCompanyCouponCount.match(/(-?\d+(\.\d+)?)/g).map(v => +v);
        let resCouponPrice = parseInt(currentCompanyCouponPrice.match(/\d+/)) 
        let resRetailPrice = parseInt(currentCompanyRetailPrice.match(/\d+/)) 
        // console.log(resCurrentCompanyRetailPrice, resCurrentCompanyCouponPricet, resCurrentCompanyCouponCount)
        console.log(resCouponPrice, Number(couponPriceOt), couponPriceDo)
        console.log(Number(couponPriceOt) <= resCouponPrice && Number(couponPriceDo) >= resCouponPrice)

        // (Number(couponCountOt) >= resCouponCount[0] && Number(couponCountDo) <= resCouponCount[1])

        // || !(Number(couponCountOt) <= resCouponCount[0]) && !(Number(couponCountDo) >= resCouponCount[1])

        if  (nisha != currentCompanyNisha && nisha !="Все" 
            || valuta != currentCompanyCouponPrice.slice(-3) && valuta !="Все" 
            || checkbox.checked != !!currentCompanyPhone 
            || !(Number(couponPriceOt) <= resCouponPrice && Number(couponPriceDo) >= resCouponPrice)
            || !(Number(retailPriceOt) <= resRetailPrice && Number(retailPriceDo) >= resRetailPrice)
            || (Number(couponCountOt) < resCouponCount[0] && Number(couponCountDo) < resCouponCount[0])
            || (Number(couponCountDo) > resCouponCount[1] && Number(couponCountOt) > resCouponCount[1])
            ) {
            
            el.style.display = 'none'
            masonry = new Masonry('.grid', {
                gutter: '.gutter-sizer',
                itemSelector: '.grid-item',
                columnWidth: '.grid-sizer',
                percentPosition: true,
                transitionDuration: '0.2s', 
              });
        }   else {
            masonry = new Masonry('.grid', {
                gutter: '.gutter-sizer',
                itemSelector: '.grid-item',
                columnWidth: '.grid-sizer',
                percentPosition: true,
                transitionDuration: '0.2s', 
              });
        }

        

    //    console.log(currentCompanyTitle, currentCompanyNisha)

        // if (el.innerHTML != currentCompanyTitle) {
        //     el.closest('.company-card').style.display = 'none'
        // }
               
                
    })
            
        
})



