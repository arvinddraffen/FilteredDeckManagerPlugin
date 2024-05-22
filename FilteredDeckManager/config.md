## Configuration Options

**Note**: Restart Anki for add-on changes to take effect.

### `allow_empty`
Create a filtered deck even if it will have no cards.

---

### `reschedule`
Enable the option to reschedule cards when answered in the filtered deck.

---

### `intervals`
* `again`
    * Interval (in seconds) to use when pressing the `again` key
* `hard`
    * Interval (in seconds) to use when pressing the `hard` key
* `good`
    * Interval (in seconds) to use when pressing the `good` key

---

### `search_1`
* `order`
    * Set the ordering to use for the the first search query used for generation of a filtered deck. Values should be a number, based on the following:
        * Oldest Seen First: 0
        * Random: 1
        * Increasing Intervals: 2
        * Decreasing Intervals: 3
        * Most Lapses: 4
        * Order Added: 5
        * Order Due: 6
        * Last Added First: 7
        * Relative Overdueness: 8
* `card_limit`
    * The maximum number of cards to include for this search term when creating the filtered deck. If the number of matching cards is less than this number, all cards will be included. If the number of matching cards exceeds this number, then the number of included cards will be capped at this number.

<!-- Table extension not enabled for markdown.extensions md_in_html.

| Order Type | Value|
| ---------- | ---- |
| Oldest Seen First | 0 |
| Random | 1 |
| Increasing Intervals | 2 |
| Decreasing Intervals | 3 |
| Most Lapses | 4 |
| Order Added | 5 |
| Order Due | 6 |
| Last Added First | 7 |
| Relative Overdueness | 8 |

-->

---

### `search_2`
* `order`
    * Refer to the `search_1` heading.
* `card_limit`
    * Refer to the `search_1` heading.

---

### `use_global_config`
Use these configuration options globally across all new imported filtered decks rather than the configuration options included in each deck.