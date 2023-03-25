window.onload = () => {
  masonry = new Masonry(".grid", {
    gutter: ".gutter-sizer",
    itemSelector: ".grid-item",
    columnWidth: ".grid-sizer",
    percentPosition: true,
    transitionDuration: "0.2s",
  });
  document.querySelector(".Test").style.opacity = "0";
  document.querySelector(".Test").style.visibility = "hidden";
  document.querySelector(".Test").style.zIndex = "-10";
};

let currentSearch
let choices = []
let elements

window.getComputedStyle(document.querySelector('.search-pc')).display === 'none' ?
  currentSearch = '.search-input-mobile' : currentSearch = '.search-input-pc'

const renderSelect = () => {
  elements = document.querySelectorAll(".js-choice");
  elements.forEach((el,index) => {
    choices[index] = new Choices(el, {
      itemSelectText: "",
      noResultsText: "Не найдено",
    });
  });
};

let val = ''

renderSelect();

let sort = function () {
  let couponCountOt = document.getElementById("coupon-count-ot");
  let couponCountDo = document.getElementById("coupon-count-do");

  let retailPriceOt = document.getElementById("retail-price-ot");
  let retailPriceDo = document.getElementById("retail-price-do");

  let couponPriceOt = document.getElementById("coupon-price-ot");
  let couponPriceDo = document.getElementById("coupon-price-do");

  couponCountOt = couponCountOt.value
    ? couponCountOt.value
    : couponCountOt.placeholder;
  couponCountDo = couponCountDo.value
    ? couponCountDo.value
    : couponCountDo.placeholder;

  retailPriceOt = retailPriceOt.value
    ? retailPriceOt.value
    : retailPriceOt.placeholder;
  retailPriceDo = retailPriceDo.value
    ? retailPriceDo.value
    : retailPriceDo.placeholder;

  couponPriceOt = couponPriceOt.value
    ? couponPriceOt.value
    : couponPriceOt.placeholder;
  couponPriceDo = couponPriceDo.value
    ? couponPriceDo.value
    : couponPriceDo.placeholder;

  const checkbox = document.getElementById("phone");
  const choicesOption = document.querySelectorAll("option");

  let nisha = choicesOption[0].innerHTML;
  let valuta = choicesOption[1].innerHTML;

  const allCopmanies = document.querySelectorAll(".company-card");

  allCopmanies.forEach((el) => {
    el.style.display = "block";

    const currentCompanyNisha = el.querySelector(".nisha").innerHTML;
    const currentCompanyCouponCount =
      el.querySelector(".coupon-count").innerHTML;
    const currentCompanyCouponPrice =
      el.querySelector(".coupon-price").innerHTML;
    const currentCompanyRetailPrice =
      el.querySelector(".retail-price").innerHTML;
      let currentCompanyPhone;
    if (el.querySelector(".contacts-phone")) {
      currentCompanyPhone = el.querySelector(".contacts-phone").innerHTML;
    } else currentCompanyPhone = '';
    

    let resCouponCount = currentCompanyCouponCount
      .match(/(-?\d+(\.\d+)?)/g)
      .map((v) => +v);
    let resCouponPrice = parseInt(currentCompanyCouponPrice.match(/\d+/));
    let resRetailPrice = parseInt(currentCompanyRetailPrice.match(/\d+/));

    if (
      (nisha != currentCompanyNisha && nisha != "Все") ||
      (valuta != currentCompanyCouponPrice.slice(-3) && valuta != "Все") ||
      (checkbox.checked && !currentCompanyPhone) ||
      !(
        Number(couponPriceOt) <= resCouponPrice &&
        Number(couponPriceDo) >= resCouponPrice
      ) ||
      !(
        Number(retailPriceOt) <= resRetailPrice &&
        Number(retailPriceDo) >= resRetailPrice
      ) ||
      (Number(couponCountOt) < resCouponCount[0] &&
        Number(couponCountDo) < resCouponCount[0]) ||
      (Number(couponCountDo) > resCouponCount[1] &&
        Number(couponCountOt) > resCouponCount[1])
    ) {
      el.style.display = "none";
      masonry = new Masonry(".grid", {
        gutter: ".gutter-sizer",
        itemSelector: ".grid-item",
        columnWidth: ".grid-sizer",
        percentPosition: true,
        transitionDuration: "0.2s",
      });
    } else {
      masonry = new Masonry(".grid", {
        gutter: ".gutter-sizer",
        itemSelector: ".grid-item",
        columnWidth: ".grid-sizer",
        percentPosition: true,
        transitionDuration: "0.2s",
      });
    }
  });
};

const sortButton = document.getElementById("sort-button");

const resetButton = document.getElementById("reset-button");

sortButton.addEventListener("click", (btn) => {
  showResults();
  // sort();
  let t = 0;
  let c = document.querySelectorAll(".company-card");
  c.forEach((el) => {
    if (el.style.display === "block") {
      t += 1;
    }
  });
});

resetButton.addEventListener("click", (btn) => {
  document.getElementById("phone").checked = false;
  document.getElementById("coupon-count-ot").value = '';
  document.getElementById("coupon-count-do").value = '';

  document.getElementById("retail-price-ot").value = '';
  document.getElementById("retail-price-do").value = '';

  document.getElementById("coupon-price-ot").value = '';
  document.getElementById("coupon-price-do").value = '';

  document.getElementById("coupon-count-ot").placeholder = 0;
  document.getElementById("coupon-count-do").placeholder = 9999;

  document.getElementById("retail-price-ot").placeholder = 0;
  document.getElementById("retail-price-do").placeholder = 9999;

  document.getElementById("coupon-price-ot").placeholder = 0;
  document.getElementById("coupon-price-do").placeholder = 9999;

  elements.forEach ((el,index) => {
    choices[index].setChoiceByValue('');
  })
  sort();
  document.querySelector(currentSearch).value = "";

  let t = 0;
  let c = document.querySelectorAll(".company-card");
  c.forEach((el) => {
    if (el.style.display === "block") {
      t += 1;
    }
  });
});

document.querySelector(currentSearch).oninput = function () {
  // console.log('click')
  showResults()
  // if (total === 0) {
  //   document.querySelector(".message-error").innerHTML = "Ничего не найдено";
  // } else {
  //   document.querySelector(".message-error").innerHTML = "";
  // }
};

let showResults = function () {
  val = document.querySelector(currentSearch).value.trim();
  let companies = document.querySelectorAll(".company-card");
  if (val != "") {
    sort();
    companies.forEach((el) => {
      if (
        el
          .querySelector(".company-card-name")
          .innerHTML.search(RegExp(val, "gi")) == -1 &&
        el.querySelector(".usluga").innerHTML.search(RegExp(val, "gi")) == -1
      ) {
        el.style.display = "none";
      }

      if (companies.length === 0) {
        console.log("clear");
      }
      // } else {
      //     el.style.display = 'block'
      // }
    });
  } else {
    companies.forEach((el) => {
      el.style.display = "block";
      sort();
    });
  }
  masonry = new Masonry(".grid", {
    gutter: ".gutter-sizer",
    itemSelector: ".grid-item",
    columnWidth: ".grid-sizer",
    percentPosition: true,
    transitionDuration: "0.2s",
  });
  let total = 0;
  companies.forEach((el) => {
    if (el.style.display === "block") {
      total += 1;
    }
  });
}
