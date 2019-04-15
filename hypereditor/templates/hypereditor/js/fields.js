(function () {
var MenuChooserField = function (page_search_url) {
    return {
        type: 'chooser',
        label: 'Menu Chooser',
        model: 'menu',
        chooserButtonText: 'Choose Menu',
        getItems: function(query, page, perPage, callback) {
            var str = 'q='+query + '&page='+page + '&perPage='+perPage
            fetch( page_search_url + '?' + str, {credentials: 'include'})
            .then(function(response) { return response.json() })
            .then(function(data) {
                callback({
                    total: data.total,
                    currentPage: data.current_page,
                    result: data.result,
                })
            })
        },

        displayItem: function(item) {
            return '<div class="card text-center"><div class="card-body"><h5 class="card-title">'+ item.title +'</h5></div></div>'
        },

        displaySelectedItem: function (item) {
            return '<div class="card text-center"><div class="card-body"><h5 class="card-title">'+ item.title +'</h5></div></div>'
        }
    }
}
})()
