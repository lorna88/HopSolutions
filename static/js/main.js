document.addEventListener('DOMContentLoaded', function() {

    // Setting the status of completed tasks
    function setStatusOfCompletedTasks(task_card_class) {
        const complete_checkboxes = document.querySelectorAll('.checkbox-task-complete')
        complete_checkboxes.forEach(checkbox => {
            checkbox.checked = checkbox.value === 'True';
            checkbox.addEventListener('click', function(event) {
                event.stopPropagation();
            });
            checkbox.addEventListener('change', function(event) {
                this.form.submit();
            });

            const task_card = checkbox.closest(task_card_class);
            const task_name = task_card.querySelector('.product-card__name');

            if (checkbox.value === 'True') {
                checkbox.checked = true;
                task_card.classList.add('task-completed');
                task_name.classList.add('task-completed-name');
            } else {
                checkbox.checked = false;
                task_card.classList.remove('task-completed');
                task_name.classList.remove('task-completed-name');
            }
        });
    }

    // Setting the color of tags
    // Color comes from 'main.css' and is stored in model field
    function setColorOfTags(elemClass, cssProp) {
        const tags = document.querySelectorAll(elemClass);
        tags.forEach(tag => {
            const color = tag.getAttribute('data-color');
            const colorValue = getComputedStyle(document.documentElement).getPropertyValue(color);
            tag.style[cssProp] = colorValue;
        });
    }

    // --- User Messages ---
    const messages = document.querySelectorAll('.alert');
    messages.forEach(message => {
        const icon_ref = message.querySelector('use');
        let icon_id = 'exclamation-triangle-fill';
        if (message.classList.contains('alert-info')) {
            icon_id = 'info-fill';
        }
        if (message.classList.contains('alert-success')) {
            icon_id = 'check-circle-fill';
        }
        icon_ref.setAttribute('xlink:href', '#' + icon_id);
    });

    // --- Logic for the pages with filter, search, etc. ---
    const homePageContent = document.querySelector('.main-content-grid');
    const calendarPageContent = document.querySelector('.main-content-calendar');
    if (homePageContent || calendarPageContent) {
        const keywordsList = document.querySelector('.keywords-list');
        const category_checkboxes = document.querySelectorAll('.category-checkbox');
        const tag_checkboxes = document.querySelectorAll('.tag-checkbox');

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
            const tags = urlParams.get('tags');
            const q = urlParams.get('q');
            const sort = urlParams.get('sort');

            category_checkboxes.forEach(checkbox => {
                if (categories && categories.includes(checkbox.dataset.keyword)) {
                    checkbox.checked = true;
                    checkboxChangeHandler.call(checkbox)
                }
            });
            tag_checkboxes.forEach(checkbox => {
                if (tags && tags.includes(checkbox.dataset.keyword)) {
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
            else {
                const activeSortButton = document.querySelector(`.sort-options .sort-button[data-sort="date_asc"]`);
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
//                    event.preventDefault();
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
                category_checkboxes.forEach(checkbox => {
                    if (checkbox.checked) {
                        cats.push(checkbox.dataset.keyword);
                    }
                });
                const tags = [];
                tag_checkboxes.forEach(checkbox => {
                    if (checkbox.checked) {
                        tags.push(checkbox.dataset.keyword);
                    }
                });
                const urlParams = new URLSearchParams(window.location.search);
                if (urlParams.has('page')) {urlParams.delete('page');}
                urlParams.set('categories', cats);
                urlParams.set('tags', tags);

                window.location.href = `${window.location.pathname}?` + urlParams.toString();
            });
        }

        if (keywordsList && (category_checkboxes.length > 0 || tag_checkboxes.length > 0)) {
            category_checkboxes.forEach(checkbox => {
                checkbox.addEventListener('change', checkboxChangeHandler);
            });
            tag_checkboxes.forEach(checkbox => {
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
    }

    // --- Logic for the Main Page (home.html) ---
    if (homePageContent) {
        setStatusOfCompletedTasks('.product-card');
        setColorOfTags('.tag-line', 'border-color');
    }

    // --- Logic for Task Detail Page (task-detail.html) ---
    const TaskDetailPageContent = document.querySelector('.page-product');
    if (TaskDetailPageContent) {
        setColorOfTags('.price-tag', 'background-color');

        // Set styles to completed task
        const checkbox = TaskDetailPageContent.querySelector('.checkbox-task-input');
        if (checkbox.checked) {
            const task_card = TaskDetailPageContent.querySelector('.task-info');
            const task_name = task_card.querySelector('.product-name');
            task_card.classList.add('task-completed');
            task_name.classList.add('task-completed-name');
        }

        // Subtasks logic
        const accordionTitle = document.querySelector('.accordion-title');
        if (accordionTitle) {
            accordionTitle.addEventListener('click', function() {
                this.closest('.accordion-item').classList.toggle('active');
            });
        }
        const complete_checkboxes = document.querySelectorAll('.checkbox-task-complete')
        subtasks_total = complete_checkboxes.length;
        subtasks_completed = 0;
        complete_checkboxes.forEach(checkbox => {
            checkbox.checked = checkbox.value === 'True';
            if (checkbox.checked) {subtasks_completed++;}
            checkbox.addEventListener('change', function(event) {
                this.form.submit();
            });
        });
        progress_bar = document.querySelector('.subtask-progress-bar > div');
        progress_bar_width = 100 / subtasks_total * subtasks_completed;
        progress_bar.style.width = progress_bar_width + '%';

        // Filling in tags list on modal form with response data from server
        const tagsButton = document.getElementById('showTags');
        if (tagsButton) {
            tagsButton.addEventListener('click', function() {
                fetch(this.getAttribute('href'))
                  .then(response => {
                    if (!response.ok) {
                      throw new Error('Сетевая ошибка ' + response.status);
                    }
                    return response.text();
                  })
                  .then(data => {
//                    console.log('Данные получены:', data);
                    const modal = document.getElementById('tagsModal');
                    const modalBody = modal.querySelector('.modal-body');
                    modalBody.innerHTML = data;
                    // Setting the status of tags for the task
                    const complete_checkboxes = modal.querySelectorAll('.checkbox-task-complete')
                    complete_checkboxes.forEach(checkbox => {
                        checkbox.checked = checkbox.value === 'True';
                    });
                  })
                  .catch(error => {
                    console.error('Произошла ошибка при запросе:', error);
                  });
            });
        }
    }

    // --- Logic for Calendar Page (my_day.html) ---
    if (calendarPageContent) {
        setStatusOfCompletedTasks('.calendar-task-card');
        setColorOfTags('.tag-line', 'border-color');

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

        // For the current calendar page
        chooseDate();

        // For other calendar pages
        const calendar = document.getElementById('bsb-calendar-1');
        const buttonGroup = calendar.querySelector('.btn-group');
        const calendarButtons = buttonGroup.querySelectorAll('button');
        calendarButtons.forEach(button => {
                button.addEventListener('click', chooseDate)
        });

        setColorOfTags('.tag-line', 'border-color');
    }

    // --- Logic for Authorization Pages ---
    const authPageContent = document.querySelector('.auth-page-wrapper');
    if (authPageContent) {
        // Styling input fields
        const inputFields = document.querySelectorAll('input');
        inputFields.forEach(input => {
            input.classList.add('Input');
        })
    }

    // --- Logic for Admin Pages ---
    const adminContent = document.querySelector('.admin-content');
    if (adminContent) {
        // Replacement standard select field for tags choice with tags buttons
        const tagsSelector = document.getElementById('id_tags');
        if (tagsSelector) {
            const tagsParent = tagsSelector.parentNode.parentNode;
            const tagButtonsContainer = document.createElement('div');
            tagButtonsContainer.classList.add('category-tags');
            tagsParent.appendChild(tagButtonsContainer);
            tagsSelector.parentNode.hidden = true;

            Array.from(tagsSelector.children).forEach(option => {
                const tagButton = document.createElement('button');
                tagButton.classList.add('category-tag');
                tagButton.setAttribute('type', 'button');
                tagButton.setAttribute('value', option.getAttribute('value'));
                if (option.hasAttribute('data-color')) {
                    tagButton.setAttribute('data-color', option.getAttribute('data-color'));
                }
                else {
                    tagButton.setAttribute('data-color', '--slate-200');
                }
                tagButton.textContent = option.textContent;
                if (option.hasAttribute('selected')) {
                    tagButton.classList.add('active');
                    const color = tagButton.getAttribute('data-color');
                    const colorValue = getComputedStyle(document.documentElement).getPropertyValue(color);
                    tagButton.style.backgroundColor = colorValue;
                }

                tagButton.addEventListener('click', function() {
                    if (this.classList.contains('active')) {
                        this.classList.remove('active');
                        const colorValue = getComputedStyle(document.documentElement).getPropertyValue('--slate-200');
                        this.style.backgroundColor = colorValue;
                        option.removeAttribute('selected');
                    }
                    else {
                        this.classList.add('active');
                        const color = this.getAttribute('data-color');
                        const colorValue = getComputedStyle(document.documentElement).getPropertyValue(color);
                        this.style.backgroundColor = colorValue;
                        option.setAttribute('selected', '');
                    }
                });

                tagButtonsContainer.appendChild(tagButton);
            });
        }

        // Styling input fields
        const inputFields = document.querySelectorAll('input');
        inputFields.forEach(input => {
            input.classList.add('Input');
        })

        // Styling textarea fields
        const textareaFields = document.querySelectorAll('textarea');
        textareaFields.forEach(textarea => {
            textarea.classList.add('Textarea');
        })

        // Styling select fields
        const selectFields = document.querySelectorAll('select');
        selectFields.forEach(select => {
            select.classList.add('select');
        })

        // Styling chexbox input fields
        const objectsTable = document.querySelector('table');
        const actionCheckboxInputs = objectsTable.querySelectorAll('input');
        actionCheckboxInputs.forEach(checkbox => {
            if (checkbox.getAttribute('type') === 'checkbox') {
                const parentNode = checkbox.parentNode;

                const checkmark = document.createElement('span');
                checkmark.classList.add('checkmark');

                const label = document.createElement('label');
                label.classList.add('checkbox-container');
                label.appendChild(checkbox);
                label.appendChild(checkmark);

                const checkboxField = document.createElement('div');
                checkboxField.classList.add('CheckboxField');
                checkboxField.appendChild(label);
                parentNode.appendChild(checkboxField);
            }
        })
    }
});