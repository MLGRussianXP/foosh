$(document).ready(function()
{
    var $select1=$('#city_select'),
        $select2=$('#school_select'),
        $options=$select2.find('option');
        $select1.on('change',function()
        {
            var queryset=$options.filter('[value="'+this.value+'"]')
            if (queryset.length > 0){
                $select2.html(
                    $options.filter('[value="' + this.value + '"]')
                );
            }  else {
                $select2.html('<option selected disabled="true">В этом городе нет школ, использующих нашу систему</option>');
            }
        }).trigger('change');
});