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

const renderSelect = () => {
  const elements = document.querySelectorAll(".js-choice");
  elements.forEach((el) => {
    const choices = new Choices(el, {
      itemSelectText: "",
      noResultsText: "Не найдено",
    });
  });
};

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
  const choices = document.querySelectorAll("option");

  let nisha = choices[0].innerHTML;
  let valuta = choices[1].innerHTML;

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
    const currentCompanyPhone = el.querySelector(".contacts-phone").innerHTML;

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

sortButton.addEventListener("click", (btn) => {
  sort();
  document.querySelector(".search-input").value = "";
  let t = 0;
  let c = document.querySelectorAll(".company-card");
  c.forEach((el) => {
    if (el.style.display === "block") {
      t += 1;
    }
  });
  // if (t === 0) {
  //   document.querySelector(".message-error").innerHTML = "Ничего не найдено";
  // } else {
  //   document.querySelector(".message-error").innerHTML = "";
  // }
});

let currentSearch

window.getComputedStyle(document.querySelector('.search-pc')).display === 'none' ?
  currentSearch = '.search-input-mobile' : currentSearch = '.search-input-pc'


document.querySelector(currentSearch).oninput = function () {
  console.log('click')
  let val = this.value.trim();
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
  // if (total === 0) {
  //   document.querySelector(".message-error").innerHTML = "Ничего не найдено";
  // } else {
  //   document.querySelector(".message-error").innerHTML = "";
  // }
};
