# © 2014 Serv. Tecnol. Avanzados (http://www.serviciosbaeza.com)
#        Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
# © 2015 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models, tools


class Owner(models.AbstractModel):
    _name = "base_multi_image.owner"
    _description = """ Wizard for base multi image """

    image_ids = fields.One2many(
        comodel_name="base_multi_image.image",
        inverse_name="owner_id",
        string="Images",
        domain=lambda self: [("owner_model", "=", self._name)],
        copy=True,
    )

    @api.depends("image_ids")
    def _compute_image_1920(self):
        """Get the main image for this object.

        This is provided as a compatibility layer for submodels that already
        had one image per record.
        """
        for s in self:
            if not s.image_ids:
                continue
            first = s.image_ids[:1]
            try:
                s.image_1920 = first.image_1920
            except AttributeError:
                continue

    # def _set_multi_image(self, image=False, name=False):
    #     """Save or delete the main image for this record.

    #     This is provided as a compatibility layer for submodels that already
    #     had one image per record.
    #     """
    #     # Values to save
    #     values = {
    #         "storage": "db",
    #         "file_db_store": tools.image_process(image, size=(1024, 1024)),
    #         "owner_model": self._name,
    #     }
    #     if name:
    #         values["name"] = name

    #     for s in self:
    #         if image:
    #             values["owner_id"] = s.id
    #             # Editing
    #             if s.image_ids:
    #                 s.image_ids[0].write(values)
    #             # Adding
    #             else:
    #                 values.setdefault("name", name or _("Main image"))
    #                 s.image_ids = [(0, 0, values)]
    #         # Deleting
    #         elif s.image_ids:
    #             s.image_ids[0].unlink()

    # def _inverse_multi_image_main(self):
    #     self._set_multi_image(self.image_main)

    # def _inverse_multi_image_main_medium(self):
    #     self._set_multi_image(self.image_main_medium)

    # def _inverse_multi_image_main_small(self):
    #     self._set_multi_image(self.image_main_small)

    def unlink(self):
        """Mimic `ondelete="cascade"` for multi images.

        Will be skipped if ``env.context['bypass_image_removal']`` == True
        """
        images = self.mapped("image_ids")
        result = super().unlink()
        if result and not self.env.context.get("bypass_image_removal"):
            images.unlink()
        return result
