from plone.restapi.blocks import visit_blocks

import logging
import transaction


logger = logging.getLogger("migrate_to_4")
logger.setLevel(logging.INFO)

# If you updated or extended the colors mappings, you should update this with the new values
COLOR_MAP = {
    "grey": {
        "--background-color": "#ecebeb",
    },
    "transparent": {
        "--background-color": "transparent",
    },
}


def migrate_backgroundColor(portal):
    i = 0
    for brain in portal.portal_catalog(
        object_provides="plone.restapi.behaviors.IBlocks"
    ):
        obj = brain.getObject()
        blocks = obj.blocks
        for block in visit_blocks(obj, blocks):
            if block.get("styles", False) and block["styles"].get(
                "backgroundColor", False
            ):
                new_block = block.copy()
                color = block["styles"]["backgroundColor"]
                new_block["styles"]["backgroundColor:noprefix"] = COLOR_MAP[color]
                del new_block["styles"]["backgroundColor"]
                block.clear()
                block.update(new_block)
                print(
                    f'{obj.absolute_url()} - Updated "backgroundColor" to "backgroundColor:noprefix"'
                )

        i += 1
        if not i % 100:
            logger.info(i)
            transaction.commit()
    transaction.commit()
