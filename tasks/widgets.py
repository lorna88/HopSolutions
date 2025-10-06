from django.forms import SelectMultiple


class TagSelectMultiple(SelectMultiple):
    def create_option(
        self, name, value, label, selected, index, subindex=None, attrs=None
    ):
        """
        Overrides method to add option attribute - color - for tags. Used on task
        change view in the admin page.
        """
        index = str(index) if subindex is None else "%s_%s" % (index, subindex)
        option_attrs = (
            self.build_attrs(self.attrs, attrs) if self.option_inherits_attrs else {}
        )
        if selected:
            option_attrs.update(self.checked_attribute)
        if "id" in option_attrs:
            option_attrs["id"] = self.id_for_label(option_attrs["id"], index)

        try:
            obj = self.choices.queryset.get(pk=value.value)
            option_attrs['data-color'] = obj.color
        except self.choices.queryset.model.DoesNotExist:
            pass

        return {
            "name": name,
            "value": value,
            "label": label,
            "selected": selected,
            "index": index,
            "attrs": option_attrs,
            "type": self.input_type,
            "template_name": self.option_template_name,
            "wrap_label": True,
        }
