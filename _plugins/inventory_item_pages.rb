module InventoryItemPages
  class DetailPage < Jekyll::Page
    def initialize(site, base, dir, item, code)
      @site = site
      @base = base
      @dir = dir
      @name = "index.html"

      process(@name)
      read_yaml(File.join(base, "_layouts"), "inventory-item.html")

      data["layout"] = "inventory-item"
      data["title"] = item["name"] || "Inventory Item"
      data["description"] = item["description"]
      data["permalink"] = "/#{dir}/"
      data["inventory_item"] = item
      data["inventory_code"] = code
    end
  end

  class Generator < Jekyll::Generator
    priority :normal

    def generate(site)
      inventory_data = site.data.fetch("inventory-export", {})
      items = inventory_data.fetch("inventory_items", [])
      seen_codes = {}

      items.each do |item|
        next unless item["is_active"]

        code = extract_code(item["item_code"])

        unless code
          Jekyll.logger.warn("Inventory pages:", "skipping item without usable code #{item.inspect}")
          next
        end

        if seen_codes.key?(code)
          Jekyll.logger.warn(
            "Inventory pages:",
            "duplicate route code #{code} for #{item["item_code"]}; already used by #{seen_codes[code]}"
          )
          next
        end

        seen_codes[code] = item["item_code"]
        site.pages << DetailPage.new(site, site.source, File.join("m", code), item, code)
      end
    end

    private

    def extract_code(item_code)
      digits = item_code.to_s.scan(/\d/).join
      return nil if digits.empty?

      digits.length > 4 ? digits[-4, 4] : digits
    end
  end
end