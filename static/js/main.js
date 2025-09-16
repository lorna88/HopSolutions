document.addEventListener('DOMContentLoaded', function() {

    // --- General logic for all pages (Login/Logout Simulation) ---
    const loginForm = document.getElementById('login-form');
    const logoutButton = document.getElementById('logout-button');
    function checkLoginStatus() {
        if (localStorage.getItem('isLoggedIn') === 'true') {
            document.body.classList.add('user-logged-in');
        } else {
            document.body.classList .remove('user-logged-in');
        }
    }
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
//            e.preventDefault();
            localStorage.setItem('isLoggedIn', 'true');
//            const nextUrl = new URLSearchParams(window.location.search).get('next');
//            window.location.href = nextUrl || '/home';
        });
    }
    if (logoutButton) {
        logoutButton.addEventListener('click', function(e) {
//            e.preventDefault();
            localStorage.removeItem('isLoggedIn');
//            window.location.href = '/home';
        });
    }
    checkLoginStatus();


    // --- Logic for the Main Page (home.html) ---
    const homePageContent = document.querySelector('.main-content-grid');
    if (homePageContent) {
        const keywordsList = document.querySelector('.keywords-list');
        const checkboxes = document.querySelectorAll('.checkbox-group input[type="checkbox"]');

        function checkboxChangeHandler(event) {
            const keyword = this.dataset.keyword;
            if (this.checked) {
                if (!document.querySelector(`.keyword-tag[data-keyword="${keyword}"]`)) {
                    const newTag = document.createElement('span');
                    newTag.className = 'keyword-tag';
                    newTag.setAttribute('data-keyword', keyword);
                    newTag.innerHTML = `${keyword} <i class="fa-solid fa-xmark remove-keyword-icon"></i>`;
                    keywordsList.appendChild(newTag);
                }
            } else {
                const tagToRemove = document.querySelector(`.keyword-tag[data-keyword="${keyword}"]`);
                if (tagToRemove) {
                    tagToRemove.remove();
                }
            }
        }

        function updateHomePageContent() {
            const urlParams = new URLSearchParams(window.location.search);
            const categories = urlParams.get('categories');
            const q = urlParams.get('q');
            const sort = urlParams.get('sort');

            checkboxes.forEach(checkbox => {
                if (categories && categories.includes(checkbox.dataset.keyword)) {
                    checkbox.checked = true;
                    checkboxChangeHandler.call(checkbox)
                }
            });

            if (q) {
                const searchInput = document.querySelector('.search-input');
                if (searchInput) {
                    searchInput.value = q
                }
            }

            if (sort) {
                const activeSortButton = document.querySelector(`.sort-options .sort-button[data-sort="${sort}"]`);
                if (activeSortButton) {
                    activeSortButton.classList.add('active-sort');
                }
            }
        }
        updateHomePageContent();

        // 1. Sort Options Logic
        const sortButtons = document.querySelectorAll('.sort-options .sort-button');
        sortButtons.forEach(button => {
            button.addEventListener('click', function() {
                sortButtons.forEach(btn => btn.classList.remove('active-sort'));
                const urlParams = new URLSearchParams(window.location.search);
                urlParams.set('sort', this.dataset.sort);
                urlParams.set('page', 1);
                window.location.href = `${window.location.pathname}?` + urlParams.toString();
            });
        });

        // 2. Pagination Logic
        const paginationList = document.querySelector('.pagination-list');
        if (paginationList) {
            const paginationLinks = paginationList.querySelectorAll('.pagination__link');
            paginationLinks.forEach(link => {
                link.addEventListener('click', function(event) {
                    event.preventDefault();
                    paginationLinks.forEach(lnk => lnk.classList.remove('active'));
                    this.classList.add('active');
                });
            });
        }

        // 3. Filter Logic (Keywords and Checkboxes)
        const filterButton = document.querySelector('#filter-button');
        if (filterButton) {
            filterButton.addEventListener('click', function() {
                const cats = [];
                checkboxes.forEach(checkbox => {
                    if (checkbox.checked) {
                        cats.push(checkbox.dataset.keyword);
                    }
                });
                const urlParams = new URLSearchParams(window.location.search);
                if (urlParams.has('page')) {urlParams.delete('page');}
                urlParams.set('categories', cats);

                window.location.href = `${window.location.pathname}?` + urlParams.toString();
            });
        }

        if (keywordsList && checkboxes.length > 0) {
            checkboxes.forEach(checkbox => {
                checkbox.addEventListener('change', checkboxChangeHandler);
            });

            keywordsList.addEventListener('click', function(event) {
                const keywordIcon = event.target.closest('.remove-keyword-icon');
                if (keywordIcon) {
                    const keywordTag = keywordIcon.closest('.keyword-tag');
                    const keywordText = keywordTag.dataset.keyword;
                    const checkbox = document.querySelector(`.checkbox-container input[data-keyword="${keywordText}"]`);
                    if (checkbox) {
                        checkbox.checked = false;
                    }
                    keywordTag.remove();
                }
            });
        }

        // 4. Search Logic
        const searchInput = document.querySelector('.search-input');
        if (searchInput) {
            const searchButton = document.querySelector('.search-button');
            searchButton.addEventListener('click', function() {
                const urlParams = new URLSearchParams(window.location.search);
                urlParams.set('q', searchInput.value);
                urlParams.set('page', 1);
                window.location.href = `${window.location.pathname}?` + urlParams.toString();
            });
        }

        // Setting the status of completed tasks
        const complete_checkboxes = document.querySelectorAll('.checkbox-task-complete')
        complete_checkboxes.forEach(checkbox => {
            checkbox.checked = checkbox.value === 'True';
            checkbox.addEventListener('click', function(event) {
                event.stopPropagation();
            });
            checkbox.addEventListener('change', function(event) {
                this.form.submit();
            });
        });
    }

    // --- Logic for Product Detail Pages (product-*.html) ---
    const productPageContent = document.querySelector('.page-product');
    if (productPageContent) {
        // Accordion
        const accordionTitle = document.querySelector('.accordion-title');
        if (accordionTitle) {
            accordionTitle.addEventListener('click', function() {
                this.closest('.accordion-item').classList.toggle('active');
            });
        }
        // "Add to Cart" Button and Counter
        const cartControls = document.querySelector('.cart-controls');
        if (cartControls) {
            const addToCartBtn = cartControls.querySelector('#add-to-cart-btn');
            const quantityCounter = cartControls.querySelector('#quantity-counter');
            const decreaseBtn = quantityCounter.querySelector('[data-action="decrease"]');
            const increaseBtn = quantityCounter.querySelector('[data-action="increase"]');
            const quantityValueSpan = quantityCounter.querySelector('.quantity-value');
            let quantity = 0;
            function updateView() {
                if (quantity === 0) {
                    addToCartBtn.classList.remove('is-hidden');
                    quantityCounter.classList.add('is-hidden');
                } else {
                    addToCartBtn.classList.add('is-hidden');
                    quantityCounter.classList.remove('is-hidden');
                    quantityValueSpan.textContent = `${quantity} in cart`;
                }
            }
            addToCartBtn.addEventListener('click', function() { quantity = 1; updateView(); });
            decreaseBtn.addEventListener('click', function() { if (quantity > 0) { quantity--; updateView(); } });
            increaseBtn.addEventListener('click', function() { quantity++; updateView(); });
            updateView();
        }
    }

    // --- Logic for Calendar Page (my_day.html) ---
    const taskCalendarContent = document.querySelector('.task-card');
    if (taskCalendarContent) {
        // Setting the status of completed tasks
        const complete_checkboxes = document.querySelectorAll('.checkbox-task-complete')
        complete_checkboxes.forEach(checkbox => {
            checkbox.checked = checkbox.value === 'True';
            checkbox.addEventListener('click', function(event) {
                event.stopPropagation();
            });
            checkbox.addEventListener('change', function(event) {
                this.form.submit();
            });
        });

        // Highlighting chosen days in calendar
        function chooseDate() {
            const days = document.querySelectorAll('.fc-day');
            days.forEach(day => {
                day.addEventListener('click', function() {
                    days.forEach(d => d.classList.remove('fc-day-active'));
                    this.classList.add('fc-day-active');
                    date = this.getAttribute('data-date');
                    const urlParams = new URLSearchParams(window.location.search);
                    urlParams.set('date', date);
                    window.location.href = `${window.location.pathname}?` + urlParams.toString();
                });
            });
        }

        chooseDate();

        const calendar = document.getElementById('bsb-calendar-1');
        const buttonGroup = calendar.querySelector('.btn-group');
        const calendarButtons = buttonGroup.querySelectorAll('button');
        calendarButtons.forEach(button => {
                button.addEventListener('click', chooseDate)
        });
    }

    // --- Logic for Tags Page (tag-list.html) ---
    const tagsContent = document.querySelector('.tag-list');
    if (tagsContent) {
        // Setting the status of tags for the task
        const complete_checkboxes = document.querySelectorAll('.checkbox-task-complete')
        complete_checkboxes.forEach(checkbox => {
            checkbox.checked = checkbox.value === 'True';
        });
    }

    // --- Logic for Cart Page (cart.html) ---
    const cartPageContent = document.querySelector('.cart-page-wrapper');
    if (cartPageContent) {
        const cartItemsList = document.getElementById('cart-items-list');
        const cartTotalPriceElem = document.getElementById('cart-total-price');
        function updateCartTotal() {
            let total = 0;
            document.querySelectorAll('.cart-item').forEach(item => {
                const priceText = item.querySelector('[data-item-total-price]').textContent;
                if (priceText) {
                    total += parseFloat(priceText.replace('$', ''));
                }
            });
            if (cartTotalPriceElem) cartTotalPriceElem.textContent = `$${total.toFixed(2)}`;
        }
        if (cartItemsList) {
            cartItemsList.addEventListener('click', function(event) {
                const cartItem = event.target.closest('.cart-item');
                if (!cartItem) return;
                const quantityElem = cartItem.querySelector('.quantity-value-cart');
                const itemTotalElem = cartItem.querySelector('[data-item-total-price]');
                const basePrice = parseFloat(cartItem.dataset.price);
                let quantity = parseInt(quantityElem.textContent);
                if (event.target.closest('[data-action="increase"]')) {
                    quantity++;
                } else if (event.target.closest('[data-action="decrease"]')) {
                    quantity = quantity > 1 ? quantity - 1 : 0;
                }
                if (event.target.closest('[data-action="remove"]') || quantity === 0) {
                    cartItem.remove();
                } else {
                    quantityElem.textContent = quantity;
                    itemTotalElem.textContent = `$${(basePrice * quantity).toFixed(2)}`;
                }
                updateCartTotal();
            });
        }
        updateCartTotal();
    }

    // --- Logic for Account and Admin Pages ---
    const accountAdminWrapper = document.querySelector('.account-page-wrapper, .admin-page-wrapper');
    if (accountAdminWrapper) {
        // Account Page Tabs
        const accountTabs = document.querySelectorAll('.account-tab');
        const tabPanes = document.querySelectorAll('.tab-pane');
        if (accountTabs.length > 0 && tabPanes.length > 0) {
            accountTabs.forEach(tab => {
                tab.addEventListener('click', function() {
                    accountTabs.forEach(item => item.classList.remove('active'));
                    tabPanes.forEach(pane => pane.classList.remove('active'));
                    const targetPane = document.querySelector(this.dataset.tabTarget);
                    this.classList.add('active');
                    if (targetPane) targetPane.classList.add('active');
                });
            });
        }

        // Admin Panel - Category Tags
        const categoryTagsContainer = document.querySelector('.category-tags');
        if (categoryTagsContainer) {
            categoryTagsContainer.addEventListener('click', function(e) {
                const clickedTag = e.target.closest('.category-tag');
                if (clickedTag) {
                    categoryTagsContainer.querySelectorAll('.category-tag').forEach(t => t.classList.remove('active'));
                    clickedTag.classList.add('active');
                }
            });
        }

        // Image Upload Simulation
        const uploadButton = document.getElementById('upload-image-btn');
        const fileInput = document.getElementById('image-upload-input');

        if (uploadButton && fileInput) {
            uploadButton.addEventListener('click', function() {
                fileInput.click();
            });

            fileInput.addEventListener('change', function(event) {
                const file = event.target.files[0];
                if (file) {
                    const reader = new FileReader();
                    const placeholder = document.querySelector('.image-upload-placeholder');

                    reader.onload = function(e) {
                        placeholder.innerHTML = '';
                        placeholder.style.backgroundImage = `url('${e.target.result}')`;
                        placeholder.style.backgroundSize = 'cover';
                        placeholder.style.backgroundPosition = 'center';
                    }
                    reader.readAsDataURL(file);
                }
            });
        }
    }
});