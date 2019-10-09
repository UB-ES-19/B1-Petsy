'''
class ProductForm():
    class DetailView:
        fields = ('nameProduct',
                  'price',
                  'description',
                  'category'
                  )

    class CreateView:
        fields = ('nameProduct',
                  'price',
                  'description',
                  'category'
                  )

    class ProductDelete:
        fields = ('nameProduct')

    class ProductUpdate:
        fields = ('nameProduct',
                  'price',
                  'description',
                  'category'
                  )
'''